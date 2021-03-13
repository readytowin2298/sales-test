from app import app, db, User, NewAccQuest, OldAccQuest, NewAccount, OldAccount
from random import randint, choice


usernames = ['dames', 'msalazar', 'eacevado', 'tstevens', 'gnugent', 'ogobin', 'tnewby']

names = ["Eliza Ojeda",
"Vickey Scheck",
"Tonisha Jobst",
"Eusebio Mcbroom",
"Kristel Mattie",
"Sheridan Gilroy",
"Gabriel Shaner",
"Vivienne Valla",
"Yanira Herbst",
"Tamica Amezcua",
"Maryjane Mccurdy",
"Rolando Tindle",
"Domonique Laursen",
"Selina Balcom",
"Rosana Puglisi",
"Sydney Cap",
"Freda Trump",
"Candie Greene",
"Wendell Cohee",
"Kathaleen Borey",
"Annalee Muirhead",
"Cristopher Moldenhauer",
"Candice Vandergriff",
"Teofila Talkington",
"Lovetta Collis",
"Annie Zhang",
"September Pauls",
"Catina Mcgowin",
"Freeda Hostetter",
"Thad Molina",
"Faith Conforti",
"Selma Mcfarling",
"Tawanna Largent",
"Maurita Tarango",
"Clarissa Bodin",
"Keitha Blansett",
"Lynsey Allaire",
"Francina Bernardo",
"Deann Weisbrod",
"Lashell Wilhite",
"Reda Gilkes",
"Katrina Danek",
"Lai Rehberg",
"Ulrike Siegfried",
"Krystina Goldsby",
"Shirleen Gambrel",
"Jacque Padgett",
"Emeline Howes",
"Cyndy Whichard",
"Hildegarde Weisinger"]


for username in usernames:
    db.session.add(User.create(username=username, password='NxlinkC5'))
    print(f'New User {username}!')

print("Database Sync")
db.session.commit()


range(12500000, 12600000)

n = range(0, 24)
for x in n:
    j = NewAccount(
    name=choice(names),
    phone_number = '867-5309',
    new_account_num = randint(12500000, 12600000),
    old_account_num = randint(12500000, 12600000),
    equipment_present = bool(randint(0,1)),
    wants_equipment_moved = bool(randint(0,1)),
    knows_where_equipment = bool(randint(0,1)),
    eth_present = bool(randint(0,1)),
    eth_to_poe = bool(randint(0,1)),
    eth_in_port = bool(randint(0,1)),
    poe_light = bool(randint(0,1)),
    wants_managed_router = bool(randint(0,1)),
    need_router_ship = bool(randint(0,1)),
    created_by = choice(usernames)
    )
    db.session.add(j)
    print(f"Added New Account for {j.name}")

print("Database Sync")
db.session.commit()


for x in n:
    j = OldAccount(
    name=choice(names),
    phone_number = '867-5309',
    new_account_num = randint(12500000, 12600000),
    old_account_num = randint(12500000, 12600000),
    approve_transfer = True,
    equipment_present = bool(randint(0,1)),
    currently_connected = bool(randint(0,1)),
    knows_where_equipment = bool(randint(0,1)),
    eth_present = bool(randint(0,1)),
    eth_to_poe = bool(randint(0,1)),
    eth_in_port = bool(randint(0,1)),
    poe_light = bool(randint(0,1)),
    has_managed_router = bool(randint(0,1)),
    created_by = choice(usernames)
    )
    db.session.add(j)
    print(f"Added Old Account for {j.name}")

print("Database Sync")
db.session.commit()