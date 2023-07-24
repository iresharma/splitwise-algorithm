from . import User, Group

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

def get_group(group_id: str):
    group = Group.nodes.first(gid=group_id)
    return group.get_group()