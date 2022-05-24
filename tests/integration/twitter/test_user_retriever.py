import os
import unittest

from src.twitter.user import TwitterUser
from src.twitter.user_not_found import TwitterUserNotFound
from src.twitter.user_retriever import TwitterDevelopersRetriever


class TwitterDevelopersRetrieverTestCase(unittest.TestCase):
    def test_retrieves_connections_of_developers(self) -> None:
        user = TwitterDevelopersRetriever(
            api_token=os.environ["JAT_TWITTER_API_TOKEN"]
        ).user("PiotrKopalko")
        self.assertEqual(
            TwitterUser(
                "PiotrKopalko",
                followed_by=[
                    "JKlikowicz",
                    "TomaszMielcarz",
                    "dbwolski",
                    "naukajazdy2",
                    "MAntykwariat",
                    "ZbigniewKamies1",
                    "pawelglinski",
                    "Rysio73167668",
                    "kasianaga",
                    "snitstwits",
                    "przegladmediow",
                    "GrzybowskiMar",
                    "m_zdanowska",
                    "MartaMarczak_",
                    "MartaWojcicka",
                    "kot_jurek",
                    "wsurala",
                    "SGardawski",
                    "brunet_dr",
                    "Magosia26015142",
                    "J_Koscinska",
                    "Rabbi_de_Winter",
                    "GreenFieldCoder",
                    "phil_ipp_fritz",
                    "WawaBielany",
                    "YESorNO_Wlochy",
                    "AWasaznik",
                    "barb_jed",
                    "A_Orzechowski",
                    "kamilagoldyka",
                    "m_aciek",
                    "Kongres_RM",
                    "bronek89",
                    "_dkarasiewicz",
                    "OgrodzeniaDarex",
                    "LukaszWizla",
                    "MiastoUrsynow",
                    "PNastawiony",
                    "LeMarton_",
                    "MiastoJestNasze",
                    "mjarzynowski",
                    "pawelprzewlocki",
                    "JanMencwel",
                    "WKarpieszuk",
                    "ignacy",
                    "Weyzu",
                ],
                following=[
                    "JKlikowicz",
                    "TomaszMielcarz",
                    "dbwolski",
                    "naukajazdy2",
                    "MAntykwariat",
                    "ZbigniewKamies1",
                    "pawelglinski",
                    "Rysio73167668",
                    "kasianaga",
                    "snitstwits",
                    "przegladmediow",
                    "GrzybowskiMar",
                    "m_zdanowska",
                    "MartaMarczak_",
                    "MartaWojcicka",
                    "kot_jurek",
                    "wsurala",
                    "SGardawski",
                    "brunet_dr",
                    "Magosia26015142",
                    "J_Koscinska",
                    "Rabbi_de_Winter",
                    "GreenFieldCoder",
                    "phil_ipp_fritz",
                    "WawaBielany",
                    "YESorNO_Wlochy",
                    "AWasaznik",
                    "barb_jed",
                    "A_Orzechowski",
                    "kamilagoldyka",
                    "m_aciek",
                    "Kongres_RM",
                    "bronek89",
                    "_dkarasiewicz",
                    "OgrodzeniaDarex",
                    "LukaszWizla",
                    "MiastoUrsynow",
                    "PNastawiony",
                    "LeMarton_",
                    "MiastoJestNasze",
                    "mjarzynowski",
                    "pawelprzewlocki",
                    "JanMencwel",
                    "WKarpieszuk",
                    "ignacy",
                    "Weyzu",
                ],
            ),
            user,
            repr(user),
        )

    def test_returns_no_such_user_on_not_found(self):
        with self.assertRaises(TwitterUserNotFound):
            TwitterDevelopersRetriever(os.environ["JAT_TWITTER_API_TOKEN"]).user(
                username="usernameof55787"
            )
