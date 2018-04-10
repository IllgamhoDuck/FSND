from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Aimodels import Base, User, AiCatalog, Ai, AiBook, AiNews, AiMatch

if __name__ == '__main__':

    # PostgreSQL
    engine = create_engine('postgresql://catalog:ducky@localhost/ai')

    # SQlite
    # engine = create_engine('sqlite:///Ai.db')
    # Bind the engine to the metadata of the Base class so that the
    # declaratives can be accessed through a DBSession instance
    Base.metadata.bind = engine

    DBSession = sessionmaker(bind=engine)
    # A DBSession() instance establishes all conversations with the database
    # and represents a "staging zone" for all the objects loaded into the
    # database session object. Any change made against the objects in the
    # session won't be persisted into the database until you call
    # session.commit(). If you're not happy about the changes, you can
    # revert all of them back to the last commit by calling
    # session.rollback()

    session = DBSession()

    # Add the admin user

    admin = User(username='(ADMIN) DUCK',
                 email='hyunbyung87@duck.com',
                 picture='/static/admin_profile.png',
                 password_hash=('$5$rounds=535000$KO0lvG/ww5jEUFXn$owLZ4sE6.'
                                'W2z8BIiIHW4Mtc74/ZAWTRGFnYLw3CpeD9'))

    session.add(admin)
    session.commit()

    # Populating Ai Catalog

    # Populating Ai

    ai = AiCatalog(name='ai',
                   picture='/static/ai.jpg',
                   description='About the AI',
                   user_id=1)

    session.add(ai)
    session.commit()

    alphago = Ai(name='alphago',
                 picture='/static/alphago.jpeg',
                 description='Google Deepmind Go ai',
                 aicatalog=ai,
                 user_id=1)

    session.add(alphago)
    session.commit()

    watson = Ai(name='watson',
                picture='/static/watson.jpg',
                description='IBM comprehensive ai',
                aicatalog=ai,
                user_id=1)

    session.add(watson)
    session.commit()

    emily = Ai(name='emily howell',
               picture='/static/emily_howell.jpg',
               description='Music auto generating ai',
               aicatalog=ai,
               user_id=1)

    session.add(emily)
    session.commit()

    # Populating Ai book

    aibook = AiCatalog(name='aibook',
                       picture='/static/aibook.jpg',
                       description='About the AI book',
                       user_id=1)
    session.add(aibook)
    session.commit()

    aibook1 = AiBook(name=("Hands-On Machine Learning with"
                           " Scikit-Learn and TensorFlow"),
                     author='Aurelien Geron',
                     price='$35.48',
                     picture='/static/aibook1.jpg',
                     description=("Concepts, Tools, and Techniques"
                                  " to Build Intelligent Systems"),
                     aicatalog=aibook,
                     user_id=1)

    session.add(aibook1)
    session.commit()

    aibook2 = AiBook(name='How to Create a Mind',
                     author='Ray Kurzweils',
                     price='$14.36',
                     picture='/static/aibook2.jpg',
                     description='The Secret of Human Thought Revealed',
                     aicatalog=aibook,
                     user_id=1)

    session.add(aibook2)
    session.commit()

    aibook3 = AiBook(name='Life 3.0',
                     author='Max Tegmark',
                     price='$18.30',
                     picture='/static/aibook3.jpg',
                     description=("Being Human in the Age of"
                                  " Artificial Intelligence"),
                     aicatalog=aibook,
                     user_id=1)

    session.add(aibook3)
    session.commit()

    # Populating Ai news

    ainews = AiCatalog(name='ainews',
                       picture='/static/ainews.jpg',
                       description='About the AI news',
                       user_id=1)
    session.add(ainews)
    session.commit()

    ainews1 = AiNews(name=("Why Continuous Learning is the key"
                           " towards Machine Intelligence"),
                     picture='/static/ainews1.jpg',
                     description='The ai news from medium',
                     aicatalog=ainews,
                     user_id=1)

    session.add(ainews1)
    session.commit()

    ainews2 = AiNews(name=("This ICO for an AI blockchain"
                           " is the most tech-hype idea of the year"),
                     picture='/static/ainews2.jpg',
                     description='The ai news from wired',
                     aicatalog=ainews,
                     user_id=1)

    session.add(ainews2)
    session.commit()

    ainews3 = AiNews(name=("The truth behind Facebook"
                           " AI inventing a new language"),
                     picture='/static/ainews3.jpg',
                     description='The ai news from medium',
                     aicatalog=ainews,
                     user_id=1)

    session.add(ainews3)
    session.commit()

    # Populating Ai match

    aimatch = AiCatalog(name='aimatch',
                        picture='/static/alphago.jpg',
                        description='About the AI match',
                        user_id=1)
    session.add(aimatch)
    session.commit()

    aimatch1 = AiMatch(name='Google DeepMind Challenge Match',
                       participant_A='AlphaGo',
                       participant_B='Lee Sedol',
                       place='Seoul',
                       picture='/static/aimatch1.jpg',
                       description='The moon shot go challenge',
                       aicatalog=aimatch,
                       user_id=1)

    session.add(aimatch1)
    session.commit()

    aimatch2 = AiMatch(name='No-Limit Texas Holdem poker',
                       participant_A='Carnegie Mellon University DeepStack',
                       participant_B='professional poker players',
                       place='Texas',
                       picture='/static/aimatch2.jpg',
                       description='The ai won the human at poker game',
                       aicatalog=aimatch,
                       user_id=1)

    session.add(aimatch2)
    session.commit()

    print("Adding ai information done!")
