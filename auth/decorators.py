from functools import wraps

def auth(metodo):
  @wraps(metodo)
  def wrapper(self, *args, **kwargs):
    print("\n[ACESSO RESTRITO] Autenticação necessária.")
    login = input("Login: ")
    senha = input("Senha: ")

    if not self._autenticar(login, senha):
      print("Acesso negado. Credenciais inválidas.")
      return None

    print("Acesso autorizado.\n")
    return metodo(self, *args, **kwargs)
  return wrapper