import torch
import numpy as np

def make_center_anchors(anchors_in, grid_size=80, device='cpu'):
    anchors_wh = []
    for anchor_set in anchors_in:
        for i in range(0,len(anchor_set),2):
            anchors_wh.append((anchor_set[i], anchor_set[i+1]))
        
    len_anchors = len(anchors_wh)

    grid_arange = torch.arange(grid_size)
    xx, yy = torch.meshgrid(grid_arange, grid_arange)  # + 0.5  # grid center, [fmsize*fmsize,2]
    xy = torch.cat((torch.unsqueeze(xx, -1), torch.unsqueeze(yy, -1)), -1) + 0.5

    wh = torch.tensor(anchors_wh)

    xy = xy.view(grid_size, grid_size, 1, 2).expand(grid_size, grid_size, len_anchors, 2).type(torch.float32)  # center
    wh = wh.view(1, 1, len_anchors, 2).expand(grid_size, grid_size, len_anchors, 2).type(torch.float32)  # w, h
    wh = wh.expand(grid_size, grid_size, len_anchors, 2).type(torch.float32)  # w, h
    center_anchors = torch.cat([xy, wh], dim=3).to(device)
    # cy cx w h

    """
    center_anchors[0][0]
    tensor([[ 0.5000,  0.5000,  1.3221,  1.7314],
            [ 0.5000,  0.5000,  3.1927,  4.0094],
            [ 0.5000,  0.5000,  5.0559,  8.0989],
            [ 0.5000,  0.5000,  9.4711,  4.8405],
            [ 0.5000,  0.5000, 11.2364, 10.0071]], device='cuda:0')
            
    center_anchors[0][1]
    tensor([[ 1.5000,  0.5000,  1.3221,  1.7314],
            [ 1.5000,  0.5000,  3.1927,  4.0094],
            [ 1.5000,  0.5000,  5.0559,  8.0989],
            [ 1.5000,  0.5000,  9.4711,  4.8405],
            [ 1.5000,  0.5000, 11.2364, 10.0071]], device='cuda:0')
            
    center_anchors[1][0]
    tensor([[ 0.5000,  1.5000,  1.3221,  1.7314],
            [ 0.5000,  1.5000,  3.1927,  4.0094],
            [ 0.5000,  1.5000,  5.0559,  8.0989],
            [ 0.5000,  1.5000,  9.4711,  4.8405],
            [ 0.5000,  1.5000, 11.2364, 10.0071]], device='cuda:0')
    
    pytorch view has reverse index
    """

    return center_anchors, len_anchors

def center_to_corner(cxcy):
    x1y1 = cxcy[..., :2] - cxcy[..., 2:] / 2
    x2y2 = cxcy[..., :2] + cxcy[..., 2:] / 2
    return torch.cat([x1y1, x2y2], dim=-1)


def corner_to_center(xy):
    cxcy = (xy[..., 2:] + xy[..., :2]) / 2
    wh = xy[..., 2:] - xy[..., :2]
    return torch.cat([cxcy, wh], dim=-1)

def find_intersection(set_1, set_2):
    lower_bounds = torch.max(set_1[:, :2].unsqueeze(1), set_2[:, :2].unsqueeze(0))  # (n1, n2, 2)
    upper_bounds = torch.min(set_1[:, 2:].unsqueeze(1), set_2[:, 2:].unsqueeze(0))  # (n1, n2, 2)
    intersection_dims = torch.clamp(upper_bounds - lower_bounds, min=0)  # (n1, n2, 2)  
    return  intersection_dims[:, :, 0] * intersection_dims[:, :, 1]  # (n1, n2) 

def find_union(set_1, set_2, intersection):
    areas_set_1 = (set_1[:, 2] - set_1[:, 0]) * (set_1[:, 3] - set_1[:, 1])  # (n1)
    areas_set_2 = (set_2[:, 2] - set_2[:, 0]) * (set_2[:, 3] - set_2[:, 1])  # (n2)
    return areas_set_1.unsqueeze(1) + areas_set_2.unsqueeze(0) - intersection + 1e-10  # (n1, n2)



def find_jaccard_overlap(set_1, set_2):
    """
    Find the Jaccard Overlap (IoU) of every box combination between two sets of boxes that are in boundary coordinates.
    :param set_1: set 1, a tensor of dimensions (n1, 4)
    :param set_2: set 2, a tensor of dimensions (n2, 4)
    :return: Jaccard Overlap of each of the boxes in set 1 with respect to each of the boxes in set 2, a tensor of dimensions (n1, n2)
    """

    # Find intersections
    intersection = find_intersection(set_1, set_2)
    
    # Find the union
    union = find_union(set_1, set_2, intersection)

    return intersection / union  # (n1, n2)



    

def get_imitation_mask(features, kd_targets, anchors, iou_factor=0.5):
    """
    gt_box: (B, K, 4) [x_min, y_min, x_max, y_max]
    """
    #print(f"Feature size: {features.shape}")
    #print(f"Feature size 2: {features.size(2)}")
    out_size = features.size(2)
    batch_size = features.size(0)
    device = kd_targets.device

    # create init mask
    mask_batch = torch.zeros([batch_size, out_size, out_size])

    if not len(kd_targets):
        return mask_batch

    gt_boxes = [[] for i in range(batch_size)]
    for i in range(len(kd_targets)):
        gt_boxes[int(kd_targets[i, 0].data)] += [kd_targets[i, 2:].clone().detach().unsqueeze(0)]

    max_num = 0
    for i in range(batch_size):
        max_num = max(max_num, len(gt_boxes[i]))
        if len(gt_boxes[i]) == 0:
            gt_boxes[i] = torch.zeros((1, 4), device=device)
        else:
            gt_boxes[i] = torch.cat(gt_boxes[i], 0)

    for i in range(batch_size):
        # print(gt_boxes[i].device)
        if max_num - gt_boxes[i].size(0):
            gt_boxes[i] = torch.cat((gt_boxes[i], torch.zeros((max_num - gt_boxes[i].size(0), 4), device=device)), 0)
        gt_boxes[i] = gt_boxes[i].unsqueeze(0)


    gt_boxes = torch.cat(gt_boxes, 0)
    gt_boxes *= out_size

    center_anchors, num_anchors = make_center_anchors(anchors, grid_size=out_size, device=device)

    anchors = center_to_corner(center_anchors).view(-1, 4)  # (N, 4)

    gt_boxes = center_to_corner(gt_boxes)

    mask_batch = torch.zeros([batch_size, out_size, out_size], device=device)

    for i in range(batch_size):
        num_obj = gt_boxes[i].size(0)
        if not num_obj:
            continue

        IOU_map = find_jaccard_overlap(anchors, gt_boxes[i]).view(out_size, out_size, num_anchors, num_obj)
        max_iou, _ = IOU_map.view(-1, num_obj).max(dim=0)
        mask_img = torch.zeros([out_size, out_size], dtype=torch.int64, requires_grad=False).type_as(features)
        threshold = max_iou * iou_factor

        for k in range(num_obj):

            mask_per_gt = torch.sum(IOU_map[:, :, :, k] > threshold[k], dim=2)

            mask_img += mask_per_gt

            mask_img += mask_img
        mask_batch[i] = mask_img

    mask_batch = mask_batch.clamp(0, 1)
    return mask_batch  # (B, h, w)

if __name__ == "__main__":
    #np.array([0,0,0])

    """ anchors = [(1.3221, 1.73145), (3.19275, 4.00944), (5.05587, 8.09892), (9.47112, 4.84053), (11.2364, 10.0071)]
    center, numa = make_center_anchors(anchors, grid_size=1)
    print(center)
    anchors = center_to_corner(center)#.view(-1, 4)  # (N, 4)
    print(anchors)
    print(0.5-1.3221/2)
    print(0.5+1.3221/2) """

    """ anchors = torch.tensor([[0, 0, 1, 1], [1,1,1.25,1.25]])
    gt_boxex = torch.tensor([[0, 0, 1, 1], [0.5, 0.5, 1, 1], [1, 1, 1.5, 1.5]])
    print(anchors.shape)
    print(gt_boxex.shape)
    print(find_intersection(anchors, gt_boxex)) """

    #anchors = torch.tensor([[0, 0, 1, 1], [1,1,1.5,1.5]])
    #areas_set_1 = (anchors[:, 2] - anchors[:, 0]) * (anchors[:, 3] - anchors[:, 1])  # (n1)
    #print(areas_set_1)

    #anchors = torch.tensor([[0, 0, 1, 1], [1,1,2,2]])
    #gt_boxex = torch.tensor([[0, 0, 1, 1], [0.5, 0.5, 1, 1], [1, 1, 2, 2]])
    #intersection = find_intersection(anchors, gt_boxex)
    #print(find_union(anchors, gt_boxex, intersection))