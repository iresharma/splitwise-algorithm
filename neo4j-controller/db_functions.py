from . import User

def create_user(name: str):
    user = User(name=name)
    user.save()
    return user

def create_rel(lender_id: str, borrower_id: str, amount: int):
    lender = User.nodes.first(id=lender_id)
    borrower = User.nodes.first(id=borrower_id)

    borrower.owes_to.connect(lender, {'amount': amount})
