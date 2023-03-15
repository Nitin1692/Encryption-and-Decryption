from flask import Flask, render_template, request, current_app
import rsa

app = Flask(__name__)


with open("public.pem", "rb") as f:
    publicKey = rsa.PublicKey.load_pkcs1(f.read())
with open("private.pem", "rb") as f:
    privateKey = rsa.PrivateKey.load_pkcs1(f.read())    

@app.route('/',methods=['GET'])
def hello_world():
    return render_template('index.html')

@app.route('/main',methods=['GET'])
def hello():
    return render_template('main.html')


@app.route('/',methods=['POST'])
def encrypt():
    first_name = request.form.get("encryt")
    #key = Fernet.generate_key()
    #fernet = Fernet(key)
    encMessage = rsa.encrypt(first_name.encode(),publicKey)
    with open("encrypted.message", "wb") as f:
        f.write(encMessage)
    return render_template('index.html', prediction=encMessage)


@app.route('/dec',methods=['POST'])
def decrypt():
    decMessage=""
    count=0
    val = request.form.get("decryt")
    m = bytes(val, 'UTF-8')
    text = open("encrypted.message", "rb").read()
    if type(m)==type(text):
        count =count + 1
        decMessage = rsa.decrypt(text, privateKey).decode()
    print(count)          
    return render_template('index.html', pred=decMessage)

@app.route('/image', methods=['POST'])
def imageEncryt():
    path = request.form.get("path")
    print(path)
    key = int(request.form.get("key"))
    fin = open(path, "rb")
    image = fin.read()
    fin.close()
    image = bytearray(image)
    for index,values in enumerate(image):
        image[index] = values ^ key
    fin = open(path, "wb")
    fin.write(image)
    res = "Encrpytion Done"
    return render_template('main.html', pred=res)  

@app.route('/images', methods=['POST'])
def imageDecrypt():
    path = request.form.get("path")
    print(path)
    key = int(request.form.get("key"))
    fin = open(path, "rb")
    image = fin.read()
    fin.close()
    image = bytearray(image)
    for index,values in enumerate(image):
        image[index] = values ^ key
    fin = open(path, "wb")
    fin.write(image)
    result = "Decrpytion Done"
    return render_template('main.html', prediction=result)     


if __name__ == '__main__':
    app.run(port=3000,debug=True)
