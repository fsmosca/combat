:: Gauntlet match

combat.py --engine-config-file combat.json ^
--engine config-name="Deuterium v2019.2 Elo 1900" tc=5000+50 ^
--engine config-name="Deuterium v2019.2 Elo 1800" tc=5000+50 ^
--engine config-name="Deuterium v2019.2 Elo 1700" tc=5000+50 ^
--opening file="opening/grand_swiss_2019_6plies.pgn" random=true ^
--round 50 ^
--reverse ^
--win-adjudication score=900 count=3 ^
--parallel 6

pause
