import argparse
import requests
import json

parser = argparse.ArgumentParser(
    description="Provide bitmovin variables"
)

parser.add_argument(
    "-n", "--name", metavar="name",
    required=True, help="Add file name."
)

parser.add_argument(
    "-d", "--description", metavar="description",
    required=False, help="provide description."
)

parser.add_argument(
    "-k", "--key", metavar="key",
    required=True, help="Bitmovin API Key."
)

parser.add_argument(
    "-t", "--tenant", metavar="tenant",
    required=True, help="Bitmovin tenant id."
)

parser.add_argument(
    "-i", "--input", metavar="input",
    required=True, help="Bitmovin input id."
)

parser.add_argument(
    "-o", "--output", metavar="output",
    required=True, help="Bitmovin output id."
)

parser.add_argument(
    "-iPath", "--inputPath", metavar="inputPath",
    required=True, help="Input Path."
)

parser.add_argument(
    "-oPath", "--outputPath", metavar="outputPath",
    required=True, help="output Path."
)


parser.add_argument(
    "-vc", "--videoConfig", metavar="videoConfig",
    required=True, help="Video config ID."
)

parser.add_argument(
    "-ac", "--audioConfig", metavar="audioConfig",
    required=True, help="Video config ID."
)

args = parser.parse_args()
asset_name=args.name
asset_description=args.description
bitmovin_api_key=args.key
bitmovin_tenant_id=args.tenant
input_id=args.input
output_id=args.output
input_path=args.inputPath
output_path=args.outputPath
video_config_id=args.videoConfig
audio_config_id=args.audioConfig

## Create Encoding

create_encoding_url = "https://api.bitmovin.com/v1/encoding/encodings"

create_encoding_payload = {
    "name": asset_name,
    "description": asset_description,
    "customData": "string", 
    "cloudRegion": "AKAMAI_US_SEA",
    "encoderVersion": "BETA",
    "encodingMode": "THREE_PASS"
}

create_encoding_headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "X-Api-Key":bitmovin_api_key,
    "X-Tenant-Org-Id":bitmovin_tenant_id
}

create_encoding_response = requests.post(create_encoding_url, json=create_encoding_payload, headers=create_encoding_headers)
create_encoding_response_json_data=create_encoding_response.json()
encodingId=create_encoding_response_json_data['data']['result']['id']
if 200<= create_encoding_response.status_code <= 299:
    print('Encoding ID successfully created!!')
else:
    print('Encodign ID creation failed!!')

## Create video stream

create_video_stream_url = "https://api.bitmovin.com/v1/encoding/encodings/" +encodingId+ "/streams"

create_video_stream_payload = {
   "inputStreams":[
      {
         "inputId":input_id,
         "inputPath":'/'+input_path,
         "selectionMode":"AUTO"
      }
   ],
   "codecConfigId":video_config_id,
    "conditions": {
    "type": "CONDITION",
    "attribute": "INPUTSTREAM",
    "operator": "==",
    "value": "TRUE"
    },
    "mode":"STANDARD"
}

create_video_stream_headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "X-Api-Key":bitmovin_api_key,
    "X-Tenant-Org-Id":bitmovin_tenant_id
}

create_video_stream_response = requests.post(create_video_stream_url, json=create_video_stream_payload, headers=create_video_stream_headers)
create_video_stream_response_json_data=create_video_stream_response.json()
videoStreamId=create_video_stream_response_json_data['data']['result']['id']
if 200<= create_video_stream_response.status_code <= 299:
    print('videoStream ID successfully created!!')
else:
    print('videoStream ID creation failed!!')

## Create audio stream

create_audio_stream_url = "https://api.bitmovin.com/v1/encoding/encodings/" +encodingId+ "/streams"

create_audio_stream_payload = {
   "inputStreams":[
      {
         "inputId":input_id,
         "inputPath":'/'+input_path,
         "selectionMode":"AUTO"
      }
   ],
   "codecConfigId":audio_config_id,
    "conditions": {
    "type": "CONDITION",
    "attribute": "INPUTSTREAM",
    "operator": "==",
    "value": "TRUE"
    },
    "mode":"STANDARD"
}

create_audio_stream_headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "X-Api-Key":bitmovin_api_key,
    "X-Tenant-Org-Id":bitmovin_tenant_id
}

create_audio_stream_response = requests.post(create_audio_stream_url, json=create_audio_stream_payload, headers=create_audio_stream_headers)
create_audio_stream_response_json_data=create_audio_stream_response.json()
audioStreamId=create_audio_stream_response_json_data['data']['result']['id']
if 200<= create_audio_stream_response.status_code <= 299:
    print('audioStream ID successfully created!!')
else:
    print('audioStream ID creation failed!!')

## Create video muxing

create_video_muxing_url = "https://api.bitmovin.com/v1/encoding/encodings/" +encodingId+ "/muxings/ts"

create_video_muxing_payload = {
   "streams":[
      {
         "streamId":videoStreamId
      }
   ],
   "outputs":[
      {
         "outputId":output_id,
         "outputPath":"/"+output_path+"//h264/video/",
         "acl":[
            {
               "permission":"PUBLIC_READ"
            }
         ]
      }
   ],
   "segmentLength":6,
   "initSegmentName":"init.mp4",
   "segmentNaming":"seg_%number%.ts"
}

create_video_muxing_headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "X-Api-Key":bitmovin_api_key,
    "X-Tenant-Org-Id":bitmovin_tenant_id
}

create_video_muxing_response = requests.post(create_video_muxing_url, json=create_video_muxing_payload, headers=create_video_muxing_headers)
create_video_muxing_response_json_data=create_video_muxing_response.json()
videoMuxingId=create_video_muxing_response_json_data['data']['result']['id']
if 200<= create_video_muxing_response.status_code <= 299:
    print('videoMuxing ID successfully created!!')
else:
    print('videoMuxing ID creation failed!!')

## Create audio muxing

create_audio_muxing_url = "https://api.bitmovin.com/v1/encoding/encodings/" +encodingId+ "/muxings/ts"

create_audio_muxing_payload = {
   "streams":[
      {
         "streamId":audioStreamId
      }
   ],
   "outputs":[
      {
         "outputId":output_id,
         "outputPath":"/"+output_path+"//h264/audio/",
         "acl":[
            {
               "permission":"PUBLIC_READ"
            }
         ]
      }
   ],
   "segmentLength":6,
   "initSegmentName":"init.mp4",
   "segmentNaming":"seg_%number%.ts"
}

create_audio_muxing_headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "X-Api-Key":bitmovin_api_key,
    "X-Tenant-Org-Id":bitmovin_tenant_id
}

create_audio_muxing_response = requests.post(create_audio_muxing_url, json=create_audio_muxing_payload, headers=create_audio_muxing_headers)
create_audio_muxing_response_json_data=create_audio_muxing_response.json()
audioMuxingId=create_audio_muxing_response_json_data['data']['result']['id']
if 200<= create_audio_muxing_response.status_code <= 299:
    print('audioMuxing ID successfully created!!')
else:
    print('audioMuxing ID creation failed!!')

## Create hls manifest

create_hls_manifest_url = "https://api.bitmovin.com/v1/encoding/manifests/hls/default"

create_hls_manifest_payload = {
   "name":output_path+"-HLS Manifest",
   "outputs":[
      {
         "outputId":output_id,
         "outputPath":"/"+output_path+"/",
         "acl":[
            {
               "permission":"PUBLIC_READ"
            }
         ]
      }
   ],
   "manifestName":"index.m3u8",
   "encodingId":encodingId
}

create_hls_manifest_headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "X-Api-Key":bitmovin_api_key,
    "X-Tenant-Org-Id":bitmovin_tenant_id
}

create_hls_manifest_response = requests.post(create_hls_manifest_url, json=create_hls_manifest_payload, headers=create_hls_manifest_headers)
create_hls_manifest_response_json_data=create_hls_manifest_response.json()
hlsManifestId=create_hls_manifest_response_json_data['data']['result']['id']
if 200<= create_hls_manifest_response.status_code <= 299:
    print('hlsManifest ID successfully created!!')
else:
    print('hlsManifest ID creation failed!!')

## Start Encoding

start_encoding_url = "https://api.bitmovin.com/v1/encoding/encodings/" +encodingId+ "/start"

start_encoding_payload = {
   "encodingMode":"THREE_PASS",
   "previewHlsManifests":[
      {
         "manifestId":hlsManifestId
      }
   ],
   "vodHlsManifests":[
      {
         "manifestId":hlsManifestId
      }
   ],
   "manifestGenerator":"V2"
}

start_encoding_headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "X-Api-Key":bitmovin_api_key,
    "X-Tenant-Org-Id":bitmovin_tenant_id
}

start_encoding_response = requests.post(start_encoding_url, json=start_encoding_payload, headers=start_encoding_headers)
start_encoding_response_json_data=start_encoding_response.json()
if 200<= start_encoding_response.status_code <= 299:
    print('Encoding started and moved to queue!!')
else:
    print('Encoding start failed!!')
