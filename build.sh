cd src
pyinstaller -F Assigner.py&
pyinstaller -F Preprocess.py&
pyinstaller -F VideoSpilt.py&
pyinstaller -F YamlGen.py&
wait
rm *.spec

cd ..
rm -r build
mkdir build
mv src/dist/* build
rm -r src/dist src/build

cp run.sh build
chmod +x build/run.sh