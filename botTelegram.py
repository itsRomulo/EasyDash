from typing import Text
import telebot
import time
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import json
import os
from App import montaGraficoVendas as mgv
from App import montaGraficoPedidos as mgp


chave_api = '5076086619:AAEdhNbePnEbzxo0fa6xPCOgeo-2H9cTxGs' #BOT Joao
#chave_api = '1966930533:AAExVlWlDPfrkZYnzLDjs3kmZgeKPyYZ8dM'
bot = telebot.TeleBot(chave_api)
meu_id = '1116879369'

# function to send image and specificy message id
bot = telegram.Bot(token=chave_api)
ultima = ''

#=================================================================================================
def send_msg(chat_ids, mensagem): # Send message
    bot.send_message(chat_id=chat_ids, text=mensagem)

#=================================================================================================
def send_captcha(chat_ids, pa ,caminho): # Send photo message
    bot.send_photo(chat_id=chat_ids,photo=open(caminho,'rb')) # send to telegram graphic image
    mensagem = 'Digite o captcha, por favor:'
    bot.send_message(chat_id=chat_ids, text=mensagem)
    mensagem = 'Responda com "/envie '+pa+' (texto captcha)"'
    bot.send_message(chat_id=chat_ids, text=mensagem)

#=================================================================================================
def envie(update, context):
        mensagem = 'Obrigado por digitar o captcha, '+str(update.message.chat.first_name)+'! 👍🏻'
        update.message.reply_text(mensagem)
        print(update)
        resposta = update.message.text #/envie 900 (captcha)
        respostaCaptcha = resposta[11:]
        senha_captcha = {"captcha":respostaCaptcha}
        respostaPA = resposta[7:10]
        file_name='Captcha.json'
        letras = ['V','W','X','Y','Z']
        # for letra in letras:
        #     monta=letra+':'
        #     if os.path.isdir(monta):
        #         pass
        #     else:
        #         os.system('C:\\Orquestrador\\mapear.bat')
        if respostaPA == '809':
            pa_path = 'W:\\Orquestrador\\65Automacao\\'+file_name
            with open(pa_path, 'w') as outfile:
                json.dump(senha_captcha, outfile)
            outfile.close()
        elif respostaPA == '900':
            pa_path = 'Y:\\Orquestrador\\65Automacao\\'+file_name
            with open(pa_path, 'w') as outfile:
                json.dump(senha_captcha, outfile)
            outfile.close()
        elif respostaPA == '292':
            pa_path = 'X:\\Orquestrador\\65Automacao\\'+file_name
            with open(pa_path, 'w') as outfile:
                json.dump(senha_captcha, outfile)
            outfile.close()
        elif respostaPA == '313':
            pa_path = 'Z:\\Orquestrador\\65Automacao\\'+file_name
            with open(pa_path, 'w') as outfile:
                json.dump(senha_captcha, outfile)
            outfile.close()
        elif respostaPA == '745':
            pa_path = 'V:\\Orquestrador\\65Automacao\\'+file_name
            with open(pa_path, 'w') as outfile:
                json.dump(senha_captcha, outfile)
            outfile.close()
        elif respostaPA == '000':
            pa_path = 'C:\\00Producao\\03PAVCRVTahto\\SalesForce\\00Dev\\'+file_name
            with open(pa_path, 'w') as outfile:
                json.dump(senha_captcha, outfile)
            outfile.close()

#=================================================================================================
def start(update, context): # welcome message
    mensagem = """
    Olá, eu sou o bot EasyDash, seu amigo para informações rápidas.
     Estou aqui para te ajudar, para isso selecione uma das opções:
        /menu -> Para mostrar o menu de opções
        /chatid -> Para que eu possa te enviar o seu chat ID do Telegram
    """
    update.message.reply_text(mensagem)

#=================================================================================================
def chatid(update, context): # Send chatid message
    mensagem = 'Olá '+str(update.message.chat.first_name)+', tudo bem? O seu chat id é '+str(update.message.chat.id)+'.'
    update.message.reply_text(mensagem)

#=================================================================================================
def oif(update, context): # Send chatid message
    mensagem = 'Olá '+str(update.message.chat.first_name)+', eu sou o bot EasyDash, seu amigo para informações rápidas! \n Digite /menu para mostrar as opções'
    update.message.reply_text(mensagem)

#================================================================================================= 
def menu(update,context):
    menu_markup = telegram.ReplyKeyboardMarkup([["VxA","VxM"],["VxS","VxD"],["VxC","PxC"],["PxM","Top10"]], one_time_keyboard=True, resize_keyboard=True)
    update.message.reply_text('Faça sua escolha, \n caso o menu não apareca clique no botão abaixo ao lado do clips ',reply_markup=menu_markup)

#=================================================================================================
def texto(update, context):
    msg = update.message.text
    global ultima
    if ultima == '':
        pass
    elif ultima == 'VxA':
        msg = msg.split(',')
        montasql=mgv.updateVxA(msg)
        grafico = mgv.montaGraficoVxA(montasql)
        grafico.write_image('VxA.png')
        bot.send_photo(chat_id=update.message.chat.id,photo=open('VxA.png','rb')) # send to telegram graphic image
        ultima=''
    elif ultima == 'VxM':
        msg=msg.split('/')
        ano=msg[0].split(',')
        mes=msg[1].split(',')
        montasql=mgv.updateVxM(ano,mes)
        grafico = mgv.montaGraficoVxM(montasql)
        grafico.write_image('VxM.png')
        bot.send_photo(chat_id=update.message.chat.id,photo=open('VxM.png','rb')) # send to telegram graphic image
        ultima=''
    elif ultima == 'VxS':
        msg=msg.split('/')
        ano=msg[0]
        mes=msg[1]
        dAno=[ano]
        dMes=[mes]
        montasql1, montasql2, montasql3, montasql4=mgv.updateVxS(dAno,dMes)
        grafico = mgv.montaGraficoVxS(montasql1, montasql2, montasql3, montasql4, mes, ano)
        grafico.write_image('VxS.png')
        bot.send_photo(chat_id=update.message.chat.id,photo=open('VxS.png','rb')) # send to telegram graphic image
        ultima=''
    elif ultima == 'VxD':
        msg=msg.split('/')
        ano=msg[0]
        mes=msg[1]
        dAno=[ano]
        dMes=[mes]
        montasql=mgv.updateVxD(dAno,dMes)
        grafico = mgv.montaGraficoVxD(montasql)
        grafico.write_image('VxD.png')
        bot.send_photo(chat_id=update.message.chat.id,photo=open('VxD.png','rb')) # send to telegram graphic image
        ultima=''
    elif ultima == 'VxC':
        msg=msg.split('/')
        ano=msg[0].split(',')
        mes=msg[1].split(',')
        montasql1, montasql2=mgv.updateVxC(ano,mes)
        grafico = mgv.montaGraficoVxC(montasql1, montasql2)
        grafico.write_image('VxC.png')
        bot.send_photo(chat_id=update.message.chat.id,photo=open('VxC.png','rb')) # send to telegram graphic image
        ultima=''
    elif ultima == 'PxC':
        msg=msg.split('/')
        ano=msg[0].split(',')
        mes=msg[1].split(',')
        montasql=mgp.updateVxCat(ano,mes)
        grafico = mgp.montaGraficoVendasCategoria(montasql)
        grafico.write_image('PxC.png')
        bot.send_photo(chat_id=update.message.chat.id,photo=open('PxC.png','rb')) # send to telegram graphic image
        ultima=''
    elif ultima == 'PxM':
        msg=msg.split('/')
        ano=msg[0].split(',')
        mes=msg[1].split(',')
        montasql=mgp.updateVxMarca(ano,mes)
        grafico = mgp.montaGraficoVendasMarca(montasql)
        grafico.write_image('PxM.png')
        bot.send_photo(chat_id=update.message.chat.id,photo=open('PxM.png','rb')) # send to telegram graphic image
        ultima=''
    elif ultima == 'Top10':
        msg=msg.split('/')
        ano=msg[0].split(',')
        mes=msg[1].split(',')
        montasql=mgp.updateTop10(ano,mes)
        grafico = mgp.montaGraficoTop10(montasql)
        grafico.write_image('Top10.png')
        bot.send_photo(chat_id=update.message.chat.id,photo=open('Top10.png','rb')) # send to telegram graphic image
        ultima=''

    if 'VxA' in msg:
        mensagem = '''Escolha os anos que deseja filtrar.
                      Exemplo: 2019,2021,2022'''
        update.message.reply_text(mensagem)
        ultima='VxA'
        # grafico = mgv.montaGraficoVxA('select sum(cast(valor_produto as float)), substring(data_venda, 7, 4) from historico_2jr GROUP BY substring(data_venda, 7, 4) ORDER BY substring(data_venda, 7, 4) ASC')
        # grafico.write_image('VxA.png')
        # bot.send_photo(chat_id=update.message.chat.id,photo=open('VxA.png','rb')) # send to telegram graphic image
    elif 'VxM' in msg:
        mensagem = '''Escolha os anos e meses que deseja filtrar.
                      Exemplo: 2019,2021/02,03'''
        update.message.reply_text(mensagem)
        ultima='VxM'
    elif 'VxS' in msg:
        mensagem = '''Escolha o ano e o mês que deseja filtrar.
                      Exemplo: 2022/03'''
        update.message.reply_text(mensagem)
        ultima='VxS'
    elif 'VxD' in msg:
        mensagem = '''Escolha o ano e o mês que deseja filtrar.
                      Exemplo: 2022/03'''
        update.message.reply_text(mensagem)
        ultima='VxD'
    elif 'VxC' in msg:
        mensagem = '''Escolha os anos e meses que deseja filtrar.
                      Exemplo: 2019,2021/02,03'''
        update.message.reply_text(mensagem)
        ultima='VxC'
    elif 'PxC' in msg:
        mensagem = '''Escolha os anos e meses que deseja filtrar.
                      Exemplo: 2019,2021/02,03'''
        update.message.reply_text(mensagem)
        ultima='PxC'
    elif 'PxM' in msg:
        mensagem = '''Escolha os anos e meses que deseja filtrar.
                      Exemplo: 2019,2021/02,03'''
        update.message.reply_text(mensagem)
        ultima='PxM'
    elif 'Top10' in msg:
        mensagem = '''Escolha os anos e meses que deseja filtrar.
                      Exemplo: 2019,2021/02,03'''
        update.message.reply_text(mensagem)
        ultima='Top10'
    
    # mensagem = 'Olá '+str(update.message.chat.first_name)+', testando qualquer mensagem!'
    # update.message.reply_text(mensagem)

#=================================================================================================
def main(): # set the direction on telegram
    updater = Updater(chave_api,use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start)) # handler /start call def start
    dp.add_handler(CommandHandler("chatid", chatid)) # handler /chatid call def chatid
    dp.add_handler(CommandHandler("menu", menu)) # handler /envie call def menu
    
    dp.add_handler(MessageHandler(Filters.text(['Chat ID','chatid','ChatID','chat id']), chatid)) # handler message Chat ID call def chatid
    dp.add_handler(MessageHandler(Filters.text(['Oi','oi','olá','Olá','opa','Opa']), oif)) # handler message Chat ID call def chatid
    dp.add_handler(MessageHandler(Filters.text, texto)) # handler any another message call def choose

    updater.start_polling() # desenv mode

    updater.idle()

if __name__ == '__main__':
    main()