`AWS Spot Price Graph <https://github.com/jeyraof/aws-spot-price-graph>`_
=========================================================================

Example
-------

.. code-block:: python

   # -*- coding: utf-8 -*-
   from spot_price_graph.api import AWSAPIWrapper
   from datetime import datetime, timedelta
   api = AWSAPIWrapper()
   query = api.ec2.describe_spot_price_history(instance_types=['t1.micro'],
                                               start_time=datetime.utcnow() - timedelta(hours=1),
                                               product_descriptions=['Linux/UNIX'],
                                               availability_zone=['ap-northeast-1a'])
   result = api.command(query)

zzz

