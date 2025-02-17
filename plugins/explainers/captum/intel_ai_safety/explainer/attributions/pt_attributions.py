
#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2023 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0
#

import torch
import numpy as np
import pandas as pd

class Captum_Saliency:
    '''
    Calculate the gradients of the output with respect to the inputs.

    Args:
      model (pytorch.nn.Module): a differentiable model to be interpreted

    Attributes:
      saliency: the captum saliency object
      grads: the gradients calculated from the saliency algorithm (created only after visualize() is called)

    Reference:
    https://captum.ai/docs/attribution_algorithms    
    '''
    def __init__(self, model) -> None:
        from captum.attr import Saliency

        self.saliency = Saliency(model)

    def visualize(self, 
                  input: torch.Tensor, 
                  labels: torch.Tensor, 
                  original_image: np.ndarray, 
                  imageTitle: str) -> None:
        '''
        Visualize the saliency result with a blended heatmap

        Args:
          input (pytorch.Tensor): the image to be used for interpretation - requires_grad must be set to True.
          labels (pytorch.Tensor): list of the label names
          original_image (numpy.ndarray): the original image to be interpreted
          imageTitle (string): title of the visualization
        '''
        from captum.attr import visualization as viz

        self.grads = self.saliency.attribute(input, target=labels.item())
        self.grads = np.transpose(
            self.grads.squeeze().cpu().detach().numpy(), (1, 2, 0)
        )
        viz.visualize_image_attr(
            self.grads,
            original_image,
            method="blended_heat_map",
            sign="absolute_value",
            show_colorbar=True,
            title=imageTitle,
        )


class Captum_IntegratedGradients:
    '''
    Approximate the integration of gradients with respect to inputs along the path from 
    a given input.

    Args:
      model (pytorch.nn.Module): a differentiable model to be interpreted

    Attributes:
      ig: the captum integrated gradients object
      attr_ig: the integrated gradients resulting from from ig.attribute() (created only after visualize() is called)
    Reference:
    https://captum.ai/docs/attribution_algorithms 
    '''
    def __init__(self, model) -> None:
        from captum.attr import IntegratedGradients

        self.ig = IntegratedGradients(model)
    def visualize(self, 
                  input: torch.Tensor, 
                  labels: torch.Tensor, 
                  original_image: np.ndarray, 
                  imageTitle: str) -> None:
        '''
        Visualize the integrated gradients result with a blended heatmap

        Args:
          input (pytorch.Tensor): the image to be used for interpretation - requires_grad must be set to True.
          labels (pytorch.Tensor): list of the label names
          original_image (numpy.ndarray): the original image to be interpreted
          imageTitle (string): title of the visualization
        '''
        from captum.attr import visualization as viz

        self.attr_ig = self.ig.attribute(input, target=labels, baselines=input * 0)
        self.attr_ig = np.transpose(
            self.attr_ig.squeeze().cpu().detach().numpy(), (1, 2, 0)
        )
        viz.visualize_image_attr(
            self.attr_ig,
            original_image,
            method="blended_heat_map",
            sign="all",
            show_colorbar=True,
            title=imageTitle,
        )


class Captum_DeepLift:
    '''
    Approximate attributions using DeepLIFT's back-propagation based algorithm.

    Args:
      model (pytorch.nn.Module): a differentiable model to be interpreted

    Attributes:
      dl: the captum deepLIFT object
      attr_dl: captum's DeepLIFT attributions resulting from dl.attribute() (created only after visualize() is called)

    Reference:
    https://captum.ai/docs/attribution_algorithms 
    '''
    def __init__(self, model) -> None:
        from captum.attr import DeepLift

        self.dl = DeepLift(model)

    def visualize(self, 
                  input: torch.Tensor, 
                  labels: torch.Tensor, 
                  original_image: np.ndarray, 
                  imageTitle: str) -> None:
        '''
        Visualize the DeepLIFT attributions with a blended heatmap

        Args:
          input (pytorch.Tensor): the image to be used for interpretation - requires_grad must be set to True.
          labels (pytorch.Tensor): list of the label names
          original_image (numpy.ndarray): the original image to be interpreted
          imageTitle (string): title of the visualization
        '''
        from captum.attr import visualization as viz

        self.attr_dl = self.dl.attribute(input, target=labels, baselines=input * 0)
        self.attr_dl = np.transpose(
            self.attr_dl.squeeze(0).cpu().detach().numpy(), (1, 2, 0)
        )
        viz.visualize_image_attr(
            self.attr_dl,
            original_image,
            method="blended_heat_map",
            sign="all",
            show_colorbar=True,
            title=imageTitle,
        )


class Captum_SmoothGrad:
    '''
    Use the Gaussian kernel to average the integrated gradients attributions via noise tunneling.

    Args:
      model (pytorch.nn.Module): a differentiable model to be interpreted

    Attributes:
      ig: the captum integrated gradients object
      nt: the captum noise tunnel object
      attr_ig_nt: resulting attributions from nt.attribute() (created only after visualize() is called)

    Reference:
    https://captum.ai/docs/attribution_algorithms 
    '''
    def __init__(self, model) -> None:
        from captum.attr import IntegratedGradients
        from captum.attr import NoiseTunnel

        self.ig = IntegratedGradients(model)
        self.nt = NoiseTunnel(self.ig)
            
    def visualize(self, 
                  input: torch.Tensor, 
                  labels: torch.Tensor, 
                  original_image: np.ndarray, 
                  imageTitle: str) -> None:
        '''
        Visualize the smooth grad attributions with a blended heatmap

        Args:
          input (pytorch.Tensor): the image to be used for interpretation - requires_grad must be set to True.
          labels (pytorch.Tensor): list of the label names
          original_image (numpy.ndarray): the original image to be interpreted
          imageTitle (string): title of the visualization
        '''
        from captum.attr import visualization as viz

        self.attr_ig_nt = self.nt.attribute(
            input,
            target=labels,
            baselines=input * 0,
            nt_type="smoothgrad_sq",
            nt_samples=100,
            stdevs=0.2,
        )
        self.attr_ig_nt = np.transpose(
            self.attr_ig_nt.squeeze(0).cpu().detach().numpy(), (1, 2, 0)
        )
        viz.visualize_image_attr(
            self.attr_ig_nt,
            original_image,
            method="blended_heat_map",
            sign="absolute_value",
            outlier_perc=10,
            show_colorbar=True,
            title=imageTitle,
        )


class Captum_FeatureAblation:
    '''
    Approximate attributions using perturbation by replacing each input feature with a reference
    value and computing the difference 

    Args:
      model (pytorch.nn.Module): a differentiable model to be interpreted

    Attributes:
      ablator: the captum feature ablation object
      fa_attr: attributes resulting from ablator.attribute() (created only after visualize() is called)
    
    Reference:
    https://captum.ai/docs/attribution_algorithms 
    '''
    def __init__(self, model) -> None:
        from captum.attr import FeatureAblation

        self.ablator = FeatureAblation(model)
    def visualize(self, 
                  input: torch.Tensor, 
                  labels: torch.Tensor, 
                  original_image: np.ndarray, 
                  imageTitle: str) -> None:
        '''
        Visualize the feature ablation attributions with a blended heatmap

        Args:
          input (pytorch.Tensor): the image to be used for interpretation - requires_grad must be set to True.
          labels (pytorch.Tensor): list of the label names
          original_image (numpy.ndarray): the original image to be interpreted
          imageTitle (string): title of the visualization
        '''
        from captum.attr import visualization as viz

        self.fa_attr = self.ablator.attribute(
            input, target=labels, baselines=input * 0
        )
        self.fa_attr = np.transpose(
            self.fa_attr.squeeze(0).cpu().detach().numpy(), (1, 2, 0)
        )
        viz.visualize_image_attr(
            self.fa_attr,
            original_image,
            method="blended_heat_map",
            sign="all",
            show_colorbar=True,
            title=imageTitle,
        )


def saliency(model):
    """
    Returns a Captum Saliency. This provides a baseline approach for computing
    input attribution, returning the gradients with respect to inputs.

    Args:
      model: pytorch model

    Returns:
      captum.attr.Saliency

    Reference:
      https://captum.ai/api/saliency.html
    """
    return Captum_Saliency(model)


def integratedgradients(model):
    """
    Returns a Captum IntegratedGradients

    Args:
      model: pytorch model

    Returns:
      captum.attr.IntegratedGradients

    Reference:
      https://captum.ai/api/integrated_gradients.html
    """
    return Captum_IntegratedGradients(model)


def deeplift(model):
    """
    Returns a Captum DeepLift

    Args:
      model: pytorch model

    Returns:
      captum.attr.DeepLift

    Reference:
      https://captum.ai/api/deep_lift.html
    """
    return Captum_DeepLift(model)


def smoothgrad(model):
    """
    Returns a Captum Integrated Gradients, Noise Tunnel SmoothGrad

    Args:
      model: pytorch model

    Returns:
      captum.attr.NoiseTunnel

    Reference:
      https://captum.ai/api/integrated_gradients.html
      https://captum.ai/api/noise_tunnel.html
    """
    return Captum_SmoothGrad(model)


def featureablation(model):
    """
    Returns a Captum FeatureAblation

    Args:
      model: pytorch model

    Returns:
      captum.attr.FeatureAblation

    Reference:
      https://captum.ai/api/feature_ablation.html
    """
    return Captum_FeatureAblation(model)
