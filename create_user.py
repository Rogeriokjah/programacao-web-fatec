from werkzeug.security import generate_password_hash, check_password_hash

# Senha em texto simples
password = "Admin123Admin"

# Gera o hash da senha
generated_hash = generate_password_hash(password, method='pbkdf2:sha256')
print("Hash gerado para a senha:", generated_hash)

# Testa se o hash gerado corresponde à senha original
is_correct_direct_check = check_password_hash(generated_hash, password)
print("Verificação direta com check_password_hash:", is_correct_direct_check)

# Testa novamente com o hash armazenado para verificar a consistência
stored_hash = generated_hash  # Simulando que 'stored_hash' é o hash armazenado
is_correct_stored_check = check_password_hash(stored_hash, password)
print("Verificação com hash armazenado:", is_correct_stored_check)
