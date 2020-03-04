:: Gauntlet match

combat.py --engine-config-file combat.json ^
--engine config-name="Deuterium v2019.2 Elo 2000" tc=5000+50 ^
--engine config-name="Deuterium v2019.2 Elo 1900" tc=5000+50 ^
--engine config-name="Deuterium v2019.2 Elo 1800" tc=5000+50 ^
--engine config-name="Deuterium v2019.2 Elo 1700" tc=5000+50 ^
--opening file="grand_swiss_2019_6plies.pgn" random=true ^
--round 50 ^
--reverse ^
--win-adjudication score=700 count=4 ^
--parallel 2

pause
