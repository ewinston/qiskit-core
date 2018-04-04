# -*- coding: utf-8 -*-
# pylint: disable=missing-param-doc,missing-type-doc
#
# Copyright 2017 IBM RESEARCH. All Rights Reserved.
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
# =============================================================================
"""
backend manager.
"""
import qiskit.backends


def register(token, url='https://quantumexperience.ng.bluemix.net/api',
             hub=None, group=None, project=None):
    """Register the backends remote backens to my backends.

    Default API is the IBM Q Experience.

    Args:
        token (str): user authentication token
        url (str): the url to the API
        hub (str): optional user hub
        group (str): optional user group
        project (str): optional user project

    Returns:
        dict: of being done
    """
    config = {
        'url': url,
        'hub': hub,
        'group': group,
        'project': project
    }
    from IBMQuantumExperience import IBMQuantumExperience
    api_temp = IBMQuantumExperience(token, config)
    qiskit.backends.discover_remote_backends(api_temp)
    # Ideally this would make not make the IBM quantum experience and register it directly
    # I want to move discover_remote_backends(api_temp) code here as i
    # dont think we need backendutils
    return {'STATUS': 'Done'}
