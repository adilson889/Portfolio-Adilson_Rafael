from flask import Flask, render_template, request, flash, redirect
import os
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'Fl4sk_S3cur3_K3y_2024_@d1ls0n_D3v_Ang0l4_!'

# Sistema de mensagens + respostas
mensagens_storage = []
respostas_storage = []

@app.route('/')
def portfolio():
    # SEUS DADOS (mantenha igual)
    dados_pessoais = {
        'nome': 'Adilson C.Rafael',
        'titulo': 'Desenvolvedor Web Full Stack',
        'email': 'adilsonrafael847@gmail.com',
        'telefone': '+244 936 838 703/ 921 325 366',
        'localizacao': 'Namibe, Angola',
        'sobre': 'Desenvolvedor Full Stack apaixonado por transformar ideias em soluções digitais inovadoras com expertise sólida em Python e Flask. Minha abordagem combina pensamento estratégico com curiosidade técnica, sempre focando em criar aplicações web robustas e escaláveis que resolvam problemas reais.Como entusiasta tecnológico, acredito que código limpo e boas práticas são a base para projetos de sucesso. Como estrategista, valorizo performance, segurança e usabilidade em cada linha escrita. E como curioso incansável, vejo cada desafio como oportunidade de crescimento e aprendizado contínuo.Especializo-me em desenvolvimento end-to-end: desde APIs RESTful e sistemas de autenticação segura até interfaces intuitivas e responsivas. Minha missão é construir pontes entre conceitos abstratos e implementações técnicas que entreguem valor tangível.Codar não é só minha profissão - é minha forma de criar impacto, resolver complexidades e evoluir constantemente no mundo digital.',
        'github': 'https://github.com/adilson889',
        'linkedin': 'https://linkedin.com/in/seuuser'
    }
    
    habilidades = [
        {'nome': 'Python', 'nivel': 50},
        {'nome': 'Flask', 'nivel': 55},
        {'nome': 'HTML/CSS', 'nivel': 80},
        {'nome': 'JavaScript', 'nivel': 70},
        {'nome': 'SQL', 'nivel': 75},
        {'nome': 'Git', 'nivel': 65}
    ]
    
    projetos = [
        {
            'titulo': 'Sistema de E-commerce',
            'descricao': 'Plataforma intermediaria com carrinho e codigo QR.',
            'tecnologias': ['HTML/JS', 'CSS', 'Supabase'],
            'link': 'https://scarrinho.netlify.app',
            'imagem': '/static/images/projeto1.jpg'
        },
        {
            'titulo': 'Sistema E-commerce',
            'descricao': 'Leitor de QR',
            'tecnologias': ['HTML', 'CSS', 'JS'],
            'link': '#',
            'imagem': '/static/images/projeto2.jpg'
        },
        {
            'titulo': 'Dashboard Analytics',
            'descricao': 'Aplicativo de controlo de vendas',
            'tecnologias': ['Python', 'Flask', 'Chart.js'],
            'link': '#',
            'imagem': '/static/images/projeto3.jpg'
        }
    ]
    
    return render_template('index.html', 
                         dados=dados_pessoais, 
                         habilidades=habilidades, 
                         projetos=projetos)

@app.route('/enviar_contato', methods=['POST'])
def enviar_contato():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        mensagem_texto = request.form['mensagem']
        
        nova_mensagem = {
            'id': len(mensagens_storage) + 1,
            'nome': nome,
            'email': email,
            'mensagem': mensagem_texto,
            'data_envio': datetime.now().strftime('%d/%m/%Y %H:%M'),
            'lida': False,
            'respondida': False
        }
        
        mensagens_storage.append(nova_mensagem)
        flash(f'✅ Obrigado {nome}! Sua mensagem foi enviada com sucesso!', 'success')
        print(f"📨 NOVA MENSAGEM: {nome} - {email}")
        
        return redirect('/')

# 🆕 ENVIAR RESPOSTA
@app.route('/enviar_resposta', methods=['POST'])
def enviar_resposta():
    if request.method == 'POST':
        mensagem_id = int(request.form['mensagem_id'])
        resposta_texto = request.form['resposta_texto']
        
        # Encontrar a mensagem original
        mensagem_original = None
        for msg in mensagens_storage:
            if msg['id'] == mensagem_id:
                mensagem_original = msg
                break
        
        if mensagem_original:
            # Salvar a resposta
            nova_resposta = {
                'id': len(respostas_storage) + 1,
                'mensagem_id': mensagem_id,
                'destinatario': mensagem_original['nome'],
                'email': mensagem_original['email'],
                'resposta': resposta_texto,
                'data_resposta': datetime.now().strftime('%d/%m/%Y %H:%M')
            }
            
            respostas_storage.append(nova_resposta)
            
            # Marcar mensagem como respondida
            mensagem_original['respondida'] = True
            mensagem_original['lida'] = True
            
            flash(f'✅ Resposta enviada para {mensagem_original["nome"]}!', 'success')
            print(f"📤 RESPOSTA ENVIADA: Para {mensagem_original['nome']}")
        
        return redirect('/admin/mensagens')

# PAINEL ADMIN
@app.route('/admin/mensagens')
def painel_mensagens():
    return render_template('admin.html', 
                         mensagens=mensagens_storage, 
                         respostas=respostas_storage)

# MARCAR COMO LIDA
@app.route('/admin/mensagem/<int:id>/lida')
def marcar_como_lida(id):
    for msg in mensagens_storage:
        if msg['id'] == id:
            msg['lida'] = True
            break
    flash('✅ Mensagem marcada como lida!', 'success')
    return redirect('/admin/mensagens')

# EXCLUIR MENSAGEM
@app.route('/admin/mensagem/<int:id>/excluir')
def excluir_mensagem(id):
    global mensagens_storage
    mensagens_storage = [msg for msg in mensagens_storage if msg['id'] != id]
    flash('🗑️ Mensagem excluída!', 'success')
    return redirect('/admin/mensagens')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)