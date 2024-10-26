# custom-config-transcoding-for-bitmovin
Python script for custom config transcoding using Bitmovin APIs

Please copy python file to a linux VM on **Linode**.
Create following configurations one time on Bitmovin using Bitmovin’s UI.

1. Create bitmoving key - command line arg -k
2. Copy Tenant id from organization details page (https://dashboard.bitmovin.com/organization/overview) - command line arg -t
3. Create input and copy input id - command line arg -i
4. Create output and copy output id - command line arg -o
5. Create video config and copy video config id - command line arg -vc
6. Create audio config and copy audio config id - command line arg -ac

Run below command from the directory where the python file is saved.

filename.py -k `Bitmovin-api-key` -t `Bitmoving-tenant-id` -i `input-id` -o `output-id` -iPath `input-path` -oPath `output-path` -vc `video-config-id` -ac `audio-config-id` -n `transcoding-name` -d `description-is-optional`

Use -h for help.
