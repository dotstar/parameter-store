import boto3
from pprint import pprint
import json


inputfile = "parameters.json"
topkey = '/mydb'
ps = boto3.client('ssm',region_name='us-east-1')


if __name__ == '__main__':
   with open(inputfile,"r") as myfile:
      data = myfile.read()
   obj = json.loads(data)

   # Initialize Parameters for Dev
   try:
      for env in ['Dev','Prod']:
         # Put login information into parameter store
         ps.put_parameter(
            Name = topkey + '/' + env + '/'+ 'Login',
            Description = "Login for " + env + "MyDB",
            Value = obj[env]['Login'],
            Type = 'String',
            Overwrite = True
         )
         # Put password information into parameter store
         ps.put_parameter(
            Name = topkey + '/' + env + '/'+ 'Password',
            Description="Password for " + env + "MyDB",
            Value = obj[env]['Password'],
            Type = 'String',
            Overwrite=True
         )
   except Exception as e:
      print(e)
      print('exiting')
      exit

   print('contents of {} key in parameter store:'.format(topkey))
   r = ps.get_parameters_by_path(
      Path=topkey,
      Recursive=True,
      MaxResults=10
   )
   print('here are your parameters, from the parameter store:')
   pprint(r['Parameters'],indent=3)

