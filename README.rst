`AWS Spot Price Graph <https://github.com/jeyraof/aws-spot-price-graph>`_
=========================================================================

Pre Setup
---------

For detail description, you could follow `this <http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html>`_.

Directly,

1. Set environment varialbes.

.. code-block:: sh

   $ export AWS_ACCESS_KEY_ID=your_access_key_id
   $ export AWS_SECRET_ACCESS_KEY=your_secret_access_key

2. Set credentials in the AWS credentials file.

.. code-block:: ini

   ; Credentials file path: ~/.aws/credentials

   [default]
   aws_access_key_id = your_access_key_id
   aws_secret_access_key = your_secret_access_key


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

