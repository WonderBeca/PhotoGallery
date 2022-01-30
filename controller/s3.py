import boto3
from flask_login import current_user
from model.database import mongo_client
# ------------------------------------------------------------------------------------------------------------------------
def s3_client():
    """
        Function: get s3 client
        Purpose: get s3 client
        :returns: s3
    """
    session = boto3.session.Session()
    client = session.client('s3')
    """ :type : pyboto3.s3 """
    return client
    
class s3Controller:
    
    # ------------------------------------------------------------------------------------------------------------------------
    def list_s3_buckets():
        """
            Function: list_s3_buckets
            Purpose: Get the list of s3 buckets
            :returns: s3 buckets in your aws account
        """
        client = s3_client()
        buckets_response = client.list_buckets()
    
        # check buckets list returned successfully
        if buckets_response['ResponseMetadata']['HTTPStatusCode'] == 200:
            for s3_buckets in buckets_response['Buckets']:
                print(f" Bucket Name: {s3_buckets['Name']} - Created on {s3_buckets['CreationDate']} \n")
        else:
            print(f" Failed while trying to get buckets list from your account")
    
    
    # ------------------------------------------------------------------------------------------------------------------------
    def s3_create_bucket(bucket_name):
        """
            function: s3_create_bucket - create s3 bucket
            :args: s3 bucket name
            :returns: bucket
        """
    
        # fetch the region
        session = boto3.session.Session()
        current_region = session.region_name
    
        print(f" You are in {current_region} AWS region..\n Bucket name passed is - {bucket_name}")
    
        s3_bucket_create_response = s3_client().create_bucket(Bucket=bucket_name,
                                                            CreateBucketConfiguration={
                                                                'LocationConstraint': current_region})
    
        print(f" Response when creating bucket - {s3_bucket_create_response} ")
        return s3_bucket_create_response

    
    # ------------------------------------------------------------------------------------------------------------------------
    def s3_delete_bucket(s3_bucket_name):
        client = s3_client()
        delete_buckets_response = client.delete_bucket(Bucket=s3_bucket_name)
    
        # check delete bucket returned successfully
        if delete_buckets_response['ResponseMetadata']['HTTPStatusCode'] == 204:
            print(f"Successfully deleted bucket {s3_bucket_name}")
        else:
            print(f"Delete bucket failed")
    
    
    # ------------------------------------------------------------------------------------------------------------------------
    def s3_version_bucket_files(s3_bucket_name):
        client = s3_client()
        version_bucket_response = client.put_bucket_versioning(Bucket=s3_bucket_name,
                                                            VersioningConfiguration={'Status': 'Enabled'})
        # check apply bucket response..
        if version_bucket_response['ResponseMetadata']['HTTPStatusCode'] == 204:
            print(f"Successfully applied Versioning to {s3_bucket_name}")
        else:
            print(f"Failed while applying Versioning to bucket")
    
    
    # ------------------------------------------------------------------------------------------------------------------------
    def s3_upload_small_files(inp_file_name, s3_bucket_name, inp_file_key, content_type):
        client = s3_client()
        upload_file_response = client.put_object(Body=inp_file_name,
                                                Bucket=s3_bucket_name,
                                                Key=inp_file_key,
                                                ContentType=content_type)
        return upload_file_response['ResponseMetadata']['HTTPHeaders']
    
    
    # ------------------------------------------------------------------------------------------------------------------------
    def s3_read_objects(s3_bucket_name, info_das_image):
        images = {}
        for i in range(len(info_das_image)):
            key = info_das_image[i]['image_hash']
            print({"image_hash": key, 'user': current_user._id})
            liked = mongo_client.get_collection('liked').find_one({"image_hash": key, 'user': current_user._id})
            if liked:
                liked = liked['liked']
            images[i] = {
                'image_link': f'https://{s3_bucket_name}.s3.sa-east-1.amazonaws.com/{key}',
                'image_owner': info_das_image[i]['user']['username'],
                'upload_date': info_das_image[i]['upload_date'],
                'image_hash': key,
                'comments': list(mongo_client.get_collection('comments').find({"image_hash": key})),
                'approved': info_das_image[i]['approved'],
                'likes': info_das_image[i]['likes'],
                'liked': 'red' if liked==True else 'black'
            }
        return images