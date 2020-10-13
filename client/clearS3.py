import boto3

s3 = boto3.resource('s3')
for b in s3.buckets.all():
    b.objects.all().delete()
    b.delete()