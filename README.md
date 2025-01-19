# photocast_cli_python

Python CLI for PhotoCast system:
## Install


```cmd
git clone https://github.com/irunart/photocast_cli_python.git
cd ./photocast_cli_python
conda create -n irun
conda activate irun
conda install docopt
conda install requests
```

## PhotoCast CLI

Show all the commands via:

```python
python photocast_cli.py
```

Execute the commands in order to display your photos via the frontend.

Note:

- Acquire photographer token from admin.
- Build photographer and build index commands only need to be executed once. Every execution is a full build to index photos under this photographer.
- Recommend to upload a folder of a few photos and run through all three commands first to check on the frontend.
- "photographer" in PhotoCast language is flat labelling system, usually configured at a granularity of `event-location-photographer`. It does not mean a "user". That means, you need to acquire a new token for a different event of a photographer.


## PhotoCast API (for developers)

API Prefix: https://photo.runart.net

Authentication:
- Put token in cookie
  - Example: `{'token': token, 'type': 'cli'}`

Endpoints:

- `POST: /upload/` -- upload photos, use multipart form with 'file' component
- `GET: /build/photographer/` -- build single photographer's photo list
- `GET: /build/index/` -- update index to include this photographer

## Example of Usage
Your path could be arranged as:
```
./
---Imgs
------image_1.jpg
------image_2.jpg
------ ···
------image_N.jpg
---pytotocat_cli_python
------photocast_cli.py
```
If you want to upload a folder of images, you can use:
```cmd
cd pytotocat_cli_python
conda activate irun
python photocast_cli.py upload your_token ../Imgs
```
