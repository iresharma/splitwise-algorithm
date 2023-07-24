from neomodel import (config, StructuredNode, StringProperty, IntegerProperty,
                      DateTimeProperty, RelationshipTo, StructuredRel, ZeroOrOne)
from os import environ
from uuid import uuid4

uri = environ.get('NEO4J_URI')
username = environ.get('NEO4J_USERNAME')
password = environ.get('NEO4J_PASSWORD')

config.DATABASE_URL = 'neo4j+s://{}:{}@{}'.format(username, password, uri)

config.AUTO_INSTALL_LABELS = True


class OwesToRelationship(StructuredRel):
    amount = IntegerProperty()
    group_id = IntegerProperty()


class Group(StructuredNode):
    name = StringProperty(required=True)
    gid = StringProperty(default=lambda: uuid4().hex)

    def get_group(self):
        results, columns = self.cypher("Match (n:Group {name: '" + self.name + "'})-[r]->(m) RETURN n, r, m;")
        rows = [row[0] for row in results]
        for i in rows:
            print(i)


class User(StructuredNode):
    name = StringProperty(required=True)
    uid = StringProperty(default=lambda: uuid4().hex)

    owes_to = RelationshipTo('User', 'OWES_TO', model=OwesToRelationship)
    groups = RelationshipTo(Group, 'PART_OF')

    def get_user(self):
        results, columns = self.cypher("MATCH (n:User {name:'" + self.name + "'})-[r]->(j) RETURN r, n, j;")
        rows = [row[0] for row in results]
        user = {
            'id': self.id,
            'name': self.name,
            'groups': [],
            'owes_to': [],
        }
        for i in rows:
            if 'User' in i.nodes[1]._labels:
                lender = i.nodes[1]._properties['name']
                amount = i._properties['amount']
                flag = True
                for j in user['owes_to']:
                    if lender in j.values():
                        j['amount'] += amount
                        flag = False
                if flag:
                    user['owes_to'].append({
                        'to': lender,
                        'amount': amount
                    })
            else:
                user['groups'].append({
                    'id': i.nodes[1]._id,
                    'name': i.nodes[1]._properties['name'],
                })
        results, columns = self.cypher("MATCH (n)-[r:OWES_TO]->(j:User {name:'" + self.name + "'}) RETURN r, n, j;")
        rows = [row[0] for row in results]
        for i in rows:
            lender = i.nodes[0]._properties['name']
            amount = i._properties['amount']
            flag = True
            for j in user['owes_to']:
                if lender in j.values():
                    j['amount'] -= amount
                    flag = False
            if flag:
                user['owes_to'].append({
                    'to': lender,
                    'amount': -amount
                })
        return user


class Transaction(StructuredNode):
    amount = IntegerProperty(required=True)
    created_at = DateTimeProperty(default_now=True)
    tid = StringProperty(default=lambda: uuid4().hex)

    lender = RelationshipTo(User, 'LENT', cardinality=ZeroOrOne)
    borrower = RelationshipTo(User, 'BORROWED')
    group = RelationshipTo(Group, 'TRANSACTION_PART_OF', cardinality=ZeroOrOne)


if __name__ == '__main__':
    # iresh = User(name="Iresh")
    # nitty = User(name="Nitty")
    # chinna = User(name="chinna")
    #
    # iresh.save()
    # nitty.save()
    # chinna.save()
    #
    # rel = iresh.owes_to.connect(nitty, {'amount': 100, 'group_id': None})
    # trans1 = Transaction(amount=100)
    # trans1.save()
    # trans1.lender.connect(nitty)
    # trans1.borrower.connect(iresh)
    # trans1.save()
    # rel2 = iresh.owes_to.connect(chinna, {'amount': 100, 'group_id': None})
    # trans2 = Transaction(amount=100)
    # trans2.save()
    # trans2.lender.connect(chinna)
    # trans2.borrower.connect(iresh)
    # trans2.save()
    # rel3 = chinna.owes_to.connect(nitty, {'amount': 100, 'group_id': None})
    # trans3 = Transaction(amount=100)
    # trans3.save()
    # trans3.lender.connect(nitty)
    # trans3.borrower.connect(chinna)
    # trans3.save()
    #
    # group1 = Group(name="Group1")
    # group1.save()
    # rel4 = iresh.groups.connect(group1)
    # rel.save()
    # rel2.save()
    # rel3.save()
    # rel5 = iresh.owes_to.connect(nitty, {'amount': 100, 'group_id': group1.id})
    # trans4 = Transaction(amount=100)
    # trans4.save()
    # trans4.lender.connect(nitty)
    # trans4.borrower.connect(iresh)
    # trans4.group.connect(group1)
    # trans4.save()
    # rel5.save()
    # iresh = User.nodes.first(name="Nitty")
    # print(iresh.get_user())

    group1 = Group.nodes.first(name="Group1")
    group1.get_group()
