"""
Place the code for your architecture here...


Please provide a function srmodel() which returns your configured and initialized network.

def srmodel():
    # init model object
    ...
    # load checkpoints
    ...
    
    return model
"""
import os
import torch
import torch.nn as nn
from torch.nn import functional as F


class repnet(nn.Module):
    def __init__(self,upscale=3):
        super(repnet, self).__init__()


        self.upscale = upscale
        num_feat = 32
        down_scale = 2

        if self.upscale == 2:
           num_repconv = 1
        else :
           num_repconv = 2

        # downsample
        self.downsampler = nn.PixelUnshuffle(down_scale)

        self.body = nn.ModuleList()
        # the first conv

        #self.body.append(nn.Conv2d(3*upscale*down_scale, num_feat, 3, 1, 1))
        self.body.append(nn.Conv2d(3 * down_scale * down_scale, num_feat, 3, 1, 1)) #fix 

        activation = nn.LeakyReLU(negative_slope=0.1, inplace=True)
        self.body.append(activation)

        # the body structure
        for _ in range(num_repconv):

            self.body.append(nn.Conv2d(num_feat, num_feat, 3, 1, 1))
            self.body.append(activation)

        # the last conv

        self.body.append(nn.Conv2d(num_feat, 3 * upscale*down_scale * upscale*down_scale, 3, 1, 1))

        # upsample
        self.upsampler = nn.PixelShuffle(upscale*down_scale)

    def forward(self, x):
        out = self.downsampler(x)

        for i in range(0, len(self.body)):
            out = self.body[i](out)

        out = self.upsampler(out)
        base = F.interpolate(x, scale_factor=self.upscale, mode='bilinear')
        out += base
        return out

def srmodel():
    # init model object
   
    model = repnet(upscale=3)
    ...
    # load checkpoints
    ...
    model_path = 'repnet_x3.pth'
    model.load_state_dict(torch.load(model_path), strict=True)
    model.eval()
    for k, v in model.named_parameters():
        v.requires_grad = False
    model = model.to(device)
    return model
