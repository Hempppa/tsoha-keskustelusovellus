# "Keskustelusovellus"
Sovelluksessa on kaikki ominaisuudet mitä foorumilta tai keskustelupalstalta olettaa. Käyttäjät voivat aloittaa keskusteluketjuja ja lisätä viestejä niihin ylläpitäjien ylläpitämillä keskustelualueilla. Sovellus ei ainakaan vielä ole testattavissa fly.iossa.
### Käynnistysohjeet
Toimii aika malliohjeiden mukaisesti. Lataa repositoria ja luo ensin juurikansioon seuraavanlainen **.env** 
'''
DATABASE_URL=<tietokannan-paikallinen-osoite>
SECRET_KEY=<salainen-avain>
'''
Sitten samalla tavalla virtuaaliympäristö ja riippuvuudet
'''
python3 -m venv venv
'''
'''
source venv/bin/activate
'''
'''
pip install -r ./reuirements.txt
'''
Samoin schema.sql. *HUOM!* schema.sql poistaa käyttämänsä nimisiä taulukoita jos niitä löytää, jos tietokannassa on tärkeitä taulukoita niin kannattaa tallentaa ne ensin tai jtn. **Varmista** myös että tietokanta on avattu, tuon komennon psql täytyy toimia normaalisti (Jos postgresql asennu oli scriptillä niin start-pg.sh käynnistää).
'''
psql < schema.sql
'''
Sovelluksen voi nyt käynnistää
'''
flask run
'''
Schema.sql myös luo kaksi käyttäjää jo valmiiksi testaamista varten, "user" ja "admin", molemmilla salasanana "1234". **Jos** haluaa jostain syystä uusia ylläpitäjä käyttäjiä niin tässä vaiheessa helpointa on luoda käyttäjä selaimella ja sitten kirjoittaa suoraan tietokantaan:
'''
psql
'''
'''
UPDATE users SET admins=TRUE WHERE names=<käyttäjän nimi>;
'''
### Sovelluksen ominaisuudet (Tällä hetkellä)
- Käyttäjä näkee alkusivulla keskustelualueet 
- Käyttäjä voi myös alkusivulla kirjautua sisään tai jatkaa ilman
- Ilman kirjautumista viestejä voi silti lukea, mutta niitä ei voi lisätä
- Käyttäjä voi keskustelualueilla aloittaa viestillä uuden ketjun
- Käyttäjä voi myös lisätä viestinsä jo valmiiksi olemassa olevan ketjun jatkeeksi
- Käyttäjä voi poistaa lähettämiään viestejä
- Käyttäjä voi etsiä ketjuja ja viestejä niiden sisältämän tekstin pohjalta
- Ylläpitäjä voi lisätä keskustelualueita
### Suuret puuttuvuudet
- Keskusteluja ja keskustelualueita ei voi sulkea/poistaa
- Poistettuja viestejä ei voi palauttaa
- Kaverikutsuja ei voi hyväksyä tai hylätä, paitsi lähettämällä sellaisen takaisin
- Ulkoasu, sivu näyttää aika huonolta vielä
- Helpompi tapa lisätä ylläpitäjä käyttäjiä, tällä hetkellä vain suoraan syöttämällä tietokantaan
- Varmaan kuuluisi järjestää uusimman mukaan kaikki
- Tietoturva
    - Sovellus ei vielä tarkista käyttäjän oikeuksia tietyille sivulle, tosin esim. käyttäjäntiedot (periaatteessa vain nimi) eivät näy muille.
    - Myöskin CSRF turvaa ei vielä ole
- Koodin siisteys
    - En kerennyt ottaa pylintiä käyttöön, pääosin koodi on ihan ok, mutta parempikin saisi olla
    - Kommentointi on aika vähäistä, 
### Mahdollisia lisäyksiä puuttuvuuksien päälle
- Käyttäjien estäminen, jolloin ainakaan kaverikutsut ja dm eivät näy, ehkä pätee kaikkiin viesteihin
    - Mahdollisuus käyttäjän laittamiseen jäähylle (tai kokonaan viestinnän estäminen) ylläpitäjille
- Rajoitetut alueet/ketjut, joihin vain määrätyt käyttäjät pääsevät 
    - Voi vielä erotella suljetut ja peitetyt, missä siis suljettuihin ei pääse ilman kutsua ja peitettyjä ei edes näe ilman
    - Näihin täytyy sitten oletettavasti pystyä lisäämään ja poistamaan jäseniä
    - Rajoitetuille ketjuille täytyy olla ketjun omat ylläpitäjät.
    - Mahdollisesti ennen lisäämistä lähetettyjä viestejä ei näe
- Kuvien lähettäminen, tosin tämä on prioriteettilistan perällä
