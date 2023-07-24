from . import User

def create_user(name: str):
    user = User(name=name)
    user.save()
    return user

def create_rel(lender_id: str, borrower_id: str, amount: int):
    lender = User.nodes.first(uid=lender_id)
    borrower = User.nodes.first(uid=borrower_id)

    borrower.owes_to.connect(lender, {'amount': amount})

def get_user(user_id: str):
    user = User.nodes.first(uid=user_id)
    return user.get_user()


