# -*- coding: utf-8 -*-

from awscli.clidriver import create_clidriver
from datetime import datetime, timedelta


class AWSAPIWrapper(object):
    def __init__(self):
        self.driver = create_clidriver()

    def command(self, *args):
        self.driver.main(*args)

    @property
    def ec2(self):
        return EC2()


class EC2(object):
    def __init__(self):
        self.category = 'ec2'
        self.instance_types = ['t1.micro', 'm1.small', 'm1.medium', 'm1.large', 'm1.xlarge',
                               'm3.medium', 'm3.large', 'm3.xlarge', 'm3.2xlarge',
                               't2.micro', 't2.small', 't2.medium', 'm2.xlarge',
                               'm2.2xlarge', 'm2.4xlarge',
                               'cr1.8xlarge',
                               'i2.xlarge', 'i2.2xlarge', 'i2.4xlarge', 'i2.8xlarge',
                               'hi1.4xlarge', 'hs1.8xlarge',
                               'c1.medium', 'c1.xlarge',
                               'c3.large', 'c3.xlarge', 'c3.2xlarge', 'c3.4xlarge', 'c3.8xlarge',
                               'cc1.4xlarge',
                               'cc2.8xlarge',
                               'g2.2xlarge',
                               'cg1.4xlarge',
                               'r3.large', 'r3.xlarge', 'r3.2xlarge', 'r3.4xlarge', 'r3.8xlarge',
                               ]
        self.timestamp_format = '%Y-%m-%dT%H:%M:%SZ'
        self.product_descriptions = ['Linux/UNIX',
                                     'Linux/UNIX (Amazon VPC)',
                                     'SUSE Linux',
                                     'SUSE Linux (Amazon VPC)',
                                     'Windows',
                                     'Windows (Amazon VPC)',
                                     ]
        self.availability_zone = ['ap-northeast-1a',
                                  'ap-northeast-1b',
                                  'ap-northeast-1c',
                                  ]

    def describe_spot_price_history(self,
                                    instance_types=None,
                                    start_time=None, end_time=None,
                                    product_descriptions=None,
                                    availability_zone=None):
        arguments = []
        arguments += self._dispatch_instance_types(instance_types=instance_types)
        arguments += self._dispatch_start_time(start_time=start_time)
        arguments += self._dispatch_end_time(end_time=end_time)
        arguments += self._dispatch_product_descriptions(product_descriptions=product_descriptions)
        arguments += self._dispatch_availability_zone(availability_zone=availability_zone)

        return (self.category, 'describe-spot-price-history') + tuple(arguments)

    def _dispatch_instance_types(self, instance_types=None):
        if instance_types:
            if not isinstance(instance_types, list):
                instance_types = [instance_types]

            instance_types_tmp = []
            for j in instance_types:
                if j in self.instance_types:
                    instance_types_tmp.append(j)

            if instance_types_tmp:
                return ['--instance-types'] + instance_types_tmp
        return []

    def _dispatch_start_time(self, start_time=None):
        if start_time:
            if isinstance(start_time, datetime):
                return ['--start-time', start_time.strftime(format=self.timestamp_format)]
            return ['--start-time', start_time]
        default = datetime.utcnow() - timedelta(hours=1)
        return ['--start-time', default.strftime(self.timestamp_format)]

    def _dispatch_end_time(self, end_time=None):
        if end_time:
            if isinstance(end_time, datetime):
                return ['--end-time', end_time.strftime(self.timestamp_format)]
            return ['--end-time', end_time]
        return []

    def _dispatch_product_descriptions(self, product_descriptions=None):
        if product_descriptions:
            if not isinstance(product_descriptions, list):
                product_descriptions = [product_descriptions]

            product_descriptions_tmp = []
            for j in product_descriptions:
                if j in self.product_descriptions:
                    product_descriptions_tmp.append(j)

            if product_descriptions_tmp:
                return ['--product-descriptions'] + product_descriptions_tmp
        return []

    def _dispatch_availability_zone(self, availability_zone=None):
        if availability_zone:
            if not isinstance(availability_zone, list):
                availability_zone = [availability_zone]

            availability_zone_tmp = []
            for j in availability_zone:
                if j in self.availability_zone:
                    availability_zone_tmp.append(j)

            if availability_zone_tmp:
                az = 'Name=availability-zone,Values=' + ','.join(availability_zone_tmp)
                return ['--filters', az]
        return []
