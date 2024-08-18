[1mdiff --git a/main.py b/main.py[m
[1mindex 79c87fa..14f0eb9 100644[m
[1m--- a/main.py[m
[1m+++ b/main.py[m
[36m@@ -4,6 +4,6 @@[m [mapp = Flask(__name__)[m
 [m
 @app.route('/') # Devido ao decorador, a função abaixo será executada automaticamente ao chegar nesta rota.[m
 def home():[m
[31m-    return render_template("index.html", variavel="Variavel no jinja é meio paia") # render_template pega arquivos da pasta "templates"[m
[32m+[m[32m    return render_template("index.html", variavel="Oieeee", subtitulo="Variável no Jinja") # render_template pega arquivos da pasta "templates"[m
 [m
 app.run(debug=True) # ao definir debug como True, a aplicação será recarregada sempre que uma alteração ocorrer[m
\ No newline at end of file[m
[1mdiff --git a/templates/index.html b/templates/index.html[m
[1mindex 82d1833..53895a2 100644[m
[1m--- a/templates/index.html[m
[1m+++ b/templates/index.html[m
[36m@@ -7,6 +7,15 @@[m
 </head>[m
 <body>[m
     <h1>Título da página</h1>[m
[32m+[m[32m    <h2>{{subtitulo}}</h2>[m
[32m+[m[32m    <h3>[m
[32m+[m[32m    {% if subtitulo %}[m
[32m+[m[32m        Yasmin vai aprender flask[m
[32m+[m[32m    {% endif %}[m
[32m+[m
[32m+[m[32m    </h3>[m
[32m+[m
     <p>{{variavel}}</p>[m
[32m+[m
 </body>[m
 </html>[m
\ No newline at end of file[m
