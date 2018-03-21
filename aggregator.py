# Copyright 2018 Kristi Nikolla
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

from lxml import etree
import requests

import configparser

CONFIG = None


def load_config():
    global CONFIG
    CONFIG = configparser.ConfigParser()
    CONFIG.read('etc/saml_aggregator.cfg')


def fetch_metadata():
    providers = CONFIG.get('DEFAULT', 'metadata_providers')
    providers = providers.replace(' ', '').split(',')

    metadata = []
    for provider in providers:
        r = requests.get(CONFIG.get('metadata_providers', provider))
        if 200 >= r.status_code < 300:
            metadata.append(r.text)
    return metadata


def write_output(metadata_list):
    entities = etree.Element(
        'EntitiesDescriptor',
        nsmap={None: 'urn:oasis:names:tc:SAML:2.0:metadata'}
    )
    for metadata in metadata_list:
        entity = etree.fromstring(metadata)
        entities.append(entity)

    tree = etree.ElementTree(entities)
    tree.write(CONFIG.get('DEFAULT', 'destination'), pretty_print=True)


def main():
    load_config()
    metadata = fetch_metadata()
    write_output(metadata)


if __name__ == '__main__':
    main()
