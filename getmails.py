import imaplib, email, os, shutil

user = 'pranjitchowdhury.work@gmail.com'
password = 'Shayan97@'
imap_url = 'imap.gmail.com'
senderemail = "pranjit.chowdhury@propero.in"

current = os.listdir("./")

if "attachments" in current:
    shutil.rmtree("attachments")
    
os.mkdir("attachments")
    
attachment_dir = './attachments'

def mult_byte_to_single_byte(p):
    s = p.decode('utf-8')
    btcode = s.split(" ")
    codes = []
    for x in btcode:
        codes.append(x.encode())
    return codes

def get_only_name(s):
    fileparts = s.split(".")
    extension = fileparts[-1]
    new_name = ""
    fileparts.remove(extension)
    for x in fileparts:
        new_name = new_name + x[0].upper()+x[1:].lower()
    return [new_name, extension]

def auth(user,password,imap_url):
    con = imaplib.IMAP4_SSL(imap_url)
    con.login(user,password)
    return con

def get_attachments(msg):
    i = 1
    for part in msg.walk():
        
        fileName = part.get_filename()
        if fileName is not None:
            fileName = get_only_name(fileName)[0] + f"_attachment_{i}" + f".{get_only_name(fileName)[1]}"
            print(fileName)
            if bool(fileName):
                filePath = os.path.join(attachment_dir, fileName)
                with open(filePath,'wb') as f:
                    f.write(part.get_payload(decode=True))
                    print("k")
            i = i+1
                
def search(key,value,con):
    result, data  = con.search(None,key,'"{}"'.format(value))
    return data


con = auth(user,password,imap_url)
con.select('INBOX')


total_number_of_emails = search("FROM", senderemail, con)[0]
bytecodes = mult_byte_to_single_byte(total_number_of_emails)

for x in bytecodes:
    result, data = con.fetch(x,'(RFC822)')
    raw = email.message_from_bytes(data[0][1])
    get_attachments(raw)
    
