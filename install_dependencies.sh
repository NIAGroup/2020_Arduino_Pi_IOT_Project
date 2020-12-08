while getopts e: flag
do
    case "${flag}" in
        e) environment=${OPTARG};;
    esac
done

sudo apt-get update && sudo apt-get upgrade
sudo apt-get install build-essential cmake unzip pkg-config
sudo apt-get install libjpeg-dev libpng-dev libtiff-dev
sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt-get install libxvidcore-dev libx264-dev
sudo apt-get install libgtk-3-dev
sudo apt-get install libcanberra-gtk*
sudo apt-get install libatlas-base-dev gfortran
sudo apt-get install libbluetooth-dev

if [ -z "$environment" ]    # If not in CI environment, do pip install.
then
  python3 -m pip install pip --upgrade
  python3 -m pip install -r flask_webapp/requirements.txt
else
  echo CI environment will create a python virtual environment so pip calls from here are skipped.
fi
