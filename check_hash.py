from werkzeug.security import check_password_hash

# Cole o hash gerado aqui
stored_hash = "pbkdf2:sha256:600000$dvw3G8XrabyDGDbi$5102aa1665adb71eff80d5988eaed8d558a4216f7108df3748ac1339237c31"  # Substitua pelo hash copiado do script anterior
password = "Password"  # A senha que deseja verificar

# Verifica se o hash armazenado corresponde à senha fornecida
is_correct = check_password_hash(stored_hash, password)
print("Resultado da verificação do hash armazenado:", is_correct)
