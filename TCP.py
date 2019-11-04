from tkinter import *
import socket,threading,time

fen=Tk()
fen.title('TCP Chat')
fen.geometry('1500x900')
can=Canvas(fen,width=1500,height=855,bg='Grey')
can.pack()

#Fonction Réseau
def serveur():
    sockets.listen(5)
    client, address = sockets.accept()
    log('{} connected'.format(address))
    while 1:
        response = client.recv(255).decode('utf-8')
        if response == 'Exit':
            log("Serveur close")
            client.close()
            sockets.close()
            break
        elif response != '':
            log('mec>'+str(response))

#Fonction input / output

def entrer(event):
    global inpt,waitinput,inputmsg,socketc
    if waitinput==0:
        temp=str(inpt.get())
        if temp=='Exit':
            socketc.close()
        elif client_started==1:
            log('moa>'+temp)
            socketc.send(temp.encode('utf-8'))
        else:
            log('No connection>'+temp)
    elif waitinput==1:
        inputmsg=str(inpt.get())
        log('rep>'+inputmsg)
        waitinput=0
    inpt.delete(0,'end')

def inp(msg):
    global waitinput,inputmsg
    if waitinput==0:
        log(msg)
        waitinput=1
        while waitinput == 1:
            time.sleep(0.05)
        return inputmsg
    else:
        print('Erreur, deux input en meme tps')

def log(msg):
    global logc,logt
    can.delete(logt)
    logc.append(str(msg))
    while len(logc)>maxline:
        del logc[0]
    logt=can.create_text(20,15,text=str('\n'.join(logc)),font='Arial 15',fill='Black',anchor=NW)

#Defninition variale

ip_me=str(socket.gethostbyname(socket.gethostname()))

client_started=0
waitinput,inputmsg=0,'Default'
logc=['TCP Chat','Copyright Mathieubl©','']

#Interface

rec=can.create_rectangle(10,10,1490,850,fill='Light grey')

logt=can.create_text(20,15,text=str('\n'.join(logc)),font='Arial 15',fill='Black',anchor=NW)

inpt=Entry(fen, width=750)
inpt.pack(side=LEFT,padx=15)

vscale,maxline=1,36
def scale(event):
    global vscale,maxline
    if vscale==1:
        fen.geometry('500x400')
        can.config(width=500, height=370)
        can.coords(rec,10,10,490,330)
        vscale,maxline=0,13
    elif vscale==0:
        fen.geometry('1500x900')
        can.config(width=1500, height=870)
        can.coords(rec,10,10,1490,830)
        vscale,maxline=1,36
        

#Réseau

def tcp():
    global sockets,socketc,ip_dest,port_dest,client_started
    log('Mon ip : ' + ip_me)
    
    sockets = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sockets.bind(('', int(inp('Mon port'))))
    threading.Thread(target=serveur).start()
    log('Serveur Started')

    ip_dest=inp('ip destinaire')
    port_dest=int(inp('port destinataire'))
    socketc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socketc.connect((ip_dest, port_dest))
    log('Connection on {}'.format(port_dest))
    client_started=1

threading.Thread(target=tcp).start()

#Fin Tkinter

fen.bind('<Return>',entrer)
fen.bind('<KeyPress-minus>',scale)

fen.mainloop()
