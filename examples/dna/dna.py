# Copyright 2020 Alibaba Group Holding Limited. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf
import tf_euler

from tf_euler.python.mp_utils.base_gnn import BaseGNNNet
from tf_euler.python.mp_utils.base import SuperviseModel, UnsuperviseModel


class GNN(BaseGNNNet):

    def __init__(self, conv, flow,
                 dims, fanouts, metapath,
                 feature_idx, feature_dim,
                 group_num=8, head_num=1,
                 add_self_loops=True):
        self.group_num = group_num
        self.head_num = head_num
        super(GNN, self).__init__(conv=conv,
                                  flow=flow,
                                  dims=dims,
                                  fanouts=fanouts,
                                  metapath=metapath,
                                  add_self_loops=add_self_loops)
        if not isinstance(feature_idx, list):
            feature_idx = [feature_idx]
        if not isinstance(feature_dim, list):
            feature_dim = [feature_dim]
        self.feature_idx = feature_idx
        self.feature_dim = feature_dim

    def to_x(self, n_id):
        x, = tf_euler.get_dense_feature(n_id,
                                        self.feature_idx,
                                        self.feature_dim)
        return x

    def get_conv(self, conv_class, dim):
        return conv_class(dim, groups=self.group_num, heads=self.head_num)


class DNA(SuperviseModel):
    def __init__(self, dims, metapath,
                 feature_idx, feature_dim,
                 label_idx, label_dim,
                 group_num=8, head_num=1):
        super(DNA, self).__init__(label_idx,
                                  label_dim)
        self.gnn = GNN('dna', 'full', dims, None, metapath,
                       feature_idx, feature_dim,
                       group_num=group_num, head_num=head_num)

    def embed(self, n_id):
        return self.gnn(n_id)
