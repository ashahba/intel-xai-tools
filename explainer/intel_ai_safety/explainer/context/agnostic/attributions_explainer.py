#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2024 Intel Corporation
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

from intel_ai_safety.explainer.utils.graphics.info import InfoPanel
from intel_ai_safety.explainer.base_explainer import BaseExplainer


class AttributionsExplainer(BaseExplainer):
    """
    Attributions base class to help identify the contribution
    of feature values towards a prediction through different
    explaination methods.
    """

    def __init__(self, *args):
        self.info_panel = {}

    def __call__(self, *args, **kwargs):
        pass

    def visualize(self, data):
        pass

    def get_info(self):
        """Display into panel in Jupyter Enviornment"""
        if self.info_panel:
            info = InfoPanel(**self.info_panel)
            info.show()
