import os

server_list = ["google.com", "facebook.com"]

page_ip = open("page_ip.txt", "w+")


f = open("paginas.txt")



for pagina in f:
    print(pagina)
    pagina = pagina.strip("\n")
    try:
        response = os.popen(f"ping -c 1 {pagina}").read()
        response = response.split(" ")
        if (len(response) == 1):
            continue
        ip = response[2][1:-1]
        page_ip.write(pagina + " " + ip + "\n")
        print(response[:4])

    except:
        pass
page_ip.close()