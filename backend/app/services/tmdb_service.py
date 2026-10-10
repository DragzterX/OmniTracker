from typing import List, Optional
import httpx
from ..core.config import settings
from ..models.media import MediaItem, MediaType
from .cache import cache
from .providers import generate_provider_links

# Curated Fallback Data for Global Trending TV
TRENDING_TV_GLOBAL = [
    {"id": "tv_shogun", "title": "Shōgun", "score": 9.4, "cover": "https://image.tmdb.org/t/p/w500/7O4iVfOMQmdCSxhOg1WNzG1AgYT.jpg", "genres": ["Drama", "War & Politics"], "desc": "Lord Toranaga battles for survival as his enemies unite against him in feudal Japan.", "release": "Season 1 Finale", "rel_num": 10.0, "country": "JP"},
    {"id": "tv_tlou", "title": "The Last of Us", "score": 8.9, "cover": "https://image.tmdb.org/t/p/w500/uKvVjK19h5G6m5MjwXh7y1i0Lz2.jpg", "genres": ["Drama", "Sci-Fi", "Action"], "desc": "Joel and Ellie traverse a devastated America overrun by infected and hostile survivors.", "release": "Season 2 Premiere", "rel_num": 10.0, "country": "US"},
    {"id": "tv_severance", "title": "Severance", "score": 9.1, "cover": "https://image.tmdb.org/t/p/w500/k9jqaW9iHwA7WkFpL8v7fP8b79k.jpg", "genres": ["Mystery", "Sci-Fi", "Drama"], "desc": "Lumon Industries employees uncover sinister conspiracies behind their severed memories.", "release": "Season 2 Episode 1", "rel_num": 11.0, "country": "US"},
    {"id": "tv_squid", "title": "Squid Game: Season 2", "score": 9.3, "cover": "https://image.tmdb.org/t/p/w500/dDlG1TzUgtwHP1jA4e0gX7J6y5I.jpg", "genres": ["Action", "Thriller", "Mystery"], "desc": "Player 456 Seong Gi-hun returns to the brutal arena to dismantle the game from within.", "release": "Season 2 Episode 6", "rel_num": 15.0, "country": "KR"},
    {"id": "tv_hotd", "title": "House of the Dragon", "score": 8.8, "cover": "https://image.tmdb.org/t/p/w500/t9Xke5724fqW326qkWZqxSV0P0L.jpg", "genres": ["Action", "Drama", "Fantasy"], "desc": "The Dance of the Dragons plunges the Targaryen dynasty into bloody civil war.", "release": "Season 2 Finale", "rel_num": 18.0, "country": "US"},
    {"id": "tv_stranger", "title": "Stranger Things", "score": 9.0, "cover": "https://image.tmdb.org/t/p/w500/49WJfeN0moxb9IPfGn8AIqMGskD.jpg", "genres": ["Sci-Fi", "Horror", "Drama"], "desc": "Hawkins faces the ultimate showdown against Vecna and the Upside Down.", "release": "Season 5 Premiere", "rel_num": 35.0, "country": "US"},
    {"id": "tv_bear", "title": "The Bear", "score": 9.2, "cover": "https://image.tmdb.org/t/p/w500/r6FG0ZpC2Y6k27Q7bC5Dq2N943A.jpg", "genres": ["Drama", "Comedy"], "desc": "A young fine-dining chef struggles to transform his family sandwich shop.", "release": "Season 3 Episode 10", "rel_num": 28.0, "country": "US"},
    {"id": "tv_boys", "title": "The Boys", "score": 8.9, "cover": "https://image.tmdb.org/t/p/w500/7Ns6tO3aYjppEN5P0IZg4wf7kox.jpg", "genres": ["Action", "Sci-Fi", "Dark Comedy"], "desc": "A team of vigilantes sets out to take down corrupt superheroes who abuse their superpowers.", "release": "Season 4 Finale", "rel_num": 32.0, "country": "US"},
    {"id": "tv_fallout", "title": "Fallout", "score": 9.1, "cover": "https://image.tmdb.org/t/p/w500/ansA6qQ9g9Xm1g9z9pQ1o9b6g8B.jpg", "genres": ["Sci-Fi", "Action", "Adventure"], "desc": "In a future post-apocalyptic Los Angeles, citizens must live in underground bunkers.", "release": "Season 1 Finale", "rel_num": 8.0, "country": "US"},
    {"id": "tv_arcane", "title": "Arcane: Season 2", "score": 9.8, "cover": "https://image.tmdb.org/t/p/w500/fqldf2t8ztc9aiwn397rWWcfGQi.jpg", "genres": ["Animation", "Sci-Fi", "Action"], "desc": "Amid the conflict between Piltover and Zaun, sisters fight on rival sides.", "release": "Act III Finale", "rel_num": 18.0, "country": "US"}
]

# Curated Fallback Data for All-Time Top TV
ALL_TIME_TV_GLOBAL = [
    {"id": "tv_bb", "title": "Breaking Bad", "score": 9.9, "cover": "https://image.tmdb.org/t/p/w500/ztkUQFLlC19CCMYHW9o1zWhJRNq.jpg", "genres": ["Crime", "Drama", "Thriller"], "desc": "A high school chemistry teacher diagnosed with terminal lung cancer turns to manufacturing methamphetamine.", "release": "Complete Series", "rel_num": 62.0, "country": "US"},
    {"id": "tv_wire", "title": "The Wire", "score": 9.8, "cover": "https://image.tmdb.org/t/p/w500/4lbclFySvugI51fws0GIvAQagjV.jpg", "genres": ["Crime", "Drama"], "desc": "The Baltimore drug scene, as seen through the eyes of drug dealers and law enforcement.", "release": "Complete Series", "rel_num": 60.0, "country": "US"},
    {"id": "tv_sopranos", "title": "The Sopranos", "score": 9.7, "cover": "https://image.tmdb.org/t/p/w500/7mF1f8qfR64z40B48F2l63G3W2B.jpg", "genres": ["Drama", "Crime"], "desc": "New Jersey mob boss Tony Soprano deals with personal and professional issues in his home and business life.", "release": "Complete Series", "rel_num": 86.0, "country": "US"},
    {"id": "tv_got", "title": "Game of Thrones", "score": 9.5, "cover": "https://image.tmdb.org/t/p/w500/1XS1oqL89opfnbLl8WnZY1O1uJx.jpg", "genres": ["Fantasy", "Drama", "Action"], "desc": "Nine noble families fight for control over the lands of Westeros while an ancient enemy returns.", "release": "Complete Series", "rel_num": 73.0, "country": "US"},
    {"id": "tv_chernobyl", "title": "Chernobyl", "score": 9.7, "cover": "https://image.tmdb.org/t/p/w500/hlLXt2tOPT6RRnjiUmoxyG1LTFi.jpg", "genres": ["Drama", "History"], "desc": "The true story of the catastrophic 1986 nuclear disaster and the sacrifices made to save Europe.", "release": "Miniseries Finale", "rel_num": 5.0, "country": "US"},
    {"id": "tv_bcs", "title": "Better Call Saul", "score": 9.6, "cover": "https://image.tmdb.org/t/p/w500/fC2HDm5t0kHjCGioLTT33502Pu4.jpg", "genres": ["Crime", "Drama"], "desc": "The trials and tribulations of criminal lawyer Jimmy McGill before establishing his strip-mall office.", "release": "Complete Series", "rel_num": 63.0, "country": "US"},
    {"id": "tv_band_brothers", "title": "Band of Brothers", "score": 9.8, "cover": "https://image.tmdb.org/t/p/w500/wMB42qQe0A1b9Z5xH1b3b5q1w3c.jpg", "genres": ["War", "Drama"], "desc": "The story of Easy Company of the US Army 101st Airborne Division and their mission in WWII Europe.", "release": "Complete Series", "rel_num": 10.0, "country": "US"},
    {"id": "tv_sherlock", "title": "Sherlock", "score": 9.5, "cover": "https://image.tmdb.org/t/p/w500/7WTsnDMmstAwh9cf9w1rsvUrsmr.jpg", "genres": ["Crime", "Mystery", "Drama"], "desc": "A modern update finds the famous sleuth and his doctor partner solving crime in 21st century London.", "release": "Complete Series", "rel_num": 13.0, "country": "GB"},
    {"id": "tv_avatar", "title": "Avatar: The Last Airbender", "score": 9.7, "cover": "https://image.tmdb.org/t/p/w500/cHFZA87igCOMaGqVTDCx9GQ6qYQ.jpg", "genres": ["Animation", "Fantasy", "Action"], "desc": "In a war-torn world of elemental magic, a young boy reawakens to undertake a dangerous mystic quest.", "release": "Complete Series", "rel_num": 61.0, "country": "US"},
    {"id": "tv_succession", "title": "Succession", "score": 9.5, "cover": "https://image.tmdb.org/t/p/w500/77w0v56Uq8F16lQ94f48A1Vb3c3.jpg", "genres": ["Drama"], "desc": "The Roy family is known for controlling the biggest media and entertainment company in the world.", "release": "Complete Series", "rel_num": 39.0, "country": "US"}
]

# Curated Fallback Data for Global Trending Movies
TRENDING_MOVIES_GLOBAL = [
    {"id": "movie_dune2", "title": "Dune: Part Two", "score": 9.4, "cover": "https://image.tmdb.org/t/p/w500/1pdfLvkbY9ohJlCjQH2CZjjYVvJ.jpg", "genres": ["Sci-Fi", "Adventure"], "desc": "Paul Atreides unites with Chani and the Fremen while seeking revenge against the conspirators.", "release": "Digital & Blu-ray", "rel_num": 1.0, "country": "US"},
    {"id": "movie_oppie", "title": "Oppenheimer", "score": 9.3, "cover": "https://image.tmdb.org/t/p/w500/8Gxv8gSFCU0XGDykEGv7zR1n2ua.jpg", "genres": ["Biography", "Drama", "History"], "desc": "The story of American scientist J. Robert Oppenheimer and his role in the development of the atomic bomb.", "release": "Available Now", "rel_num": 1.0, "country": "US"},
    {"id": "movie_deadpool", "title": "Deadpool & Wolverine", "score": 9.1, "cover": "https://image.tmdb.org/t/p/w500/8cdWjvZQUExUUTzyp4t6EDMubfO.jpg", "genres": ["Action", "Comedy", "Sci-Fi"], "desc": "A listless Wade Wilson toils in civilian life until a threat emerges, bringing him into orbit with Wolverine.", "release": "Home Premiere", "rel_num": 1.0, "country": "US"},
    {"id": "movie_godzilla_minus", "title": "Godzilla Minus One", "score": 9.5, "cover": "https://image.tmdb.org/t/p/w500/hkxxMIGaiCTmrEArK7J56Jv2x8O.jpg", "genres": ["Action", "Sci-Fi", "Drama"], "desc": "Post-war Japan is at its lowest point when a new crisis in the form of a giant monster rises.", "release": "Streaming Release", "rel_num": 1.0, "country": "JP"},
    {"id": "movie_inside_out2", "title": "Inside Out 2", "score": 9.0, "cover": "https://image.tmdb.org/t/p/w500/vpnVM9B6NMmQpWeZvzLvDESb2QY.jpg", "genres": ["Animation", "Family", "Adventure"], "desc": "Teenager Riley's mind headquarters undergoes a sudden demolition to make room for unexpected new Emotions.", "release": "Digital Release", "rel_num": 1.0, "country": "US"},
    {"id": "movie_furiosa", "title": "Furiosa: A Mad Max Saga", "score": 8.9, "cover": "https://image.tmdb.org/t/p/w500/iADOJ8Zymht2JPMoy3R7xUMZqaC.jpg", "genres": ["Action", "Adventure", "Sci-Fi"], "desc": "As the world falls, young Furiosa is snatched from the Green Place of Many Mothers into a Biker Horde.", "release": "Available to Rent/Buy", "rel_num": 1.0, "country": "AU"},
    {"id": "movie_spider_verse", "title": "Spider-Man: Across the Spider-Verse", "score": 9.6, "cover": "https://image.tmdb.org/t/p/w500/8Vt6mWEReuy4Of61Lnj5Xj704m8.jpg", "genres": ["Animation", "Action", "Adventure"], "desc": "Miles Morales catapults across the Multiverse, where he encounters a team of Spider-People.", "release": "Available on Streaming", "rel_num": 1.0, "country": "US"},
    {"id": "movie_poor_things", "title": "Poor Things", "score": 9.0, "cover": "https://image.tmdb.org/t/p/w500/kCGlIMHnOm8JPXq3rXM6c5wMxcT.jpg", "genres": ["Sci-Fi", "Comedy", "Romance"], "desc": "The incredible tale about the fantastical evolution of Bella Baxter, a young woman brought back to life.", "release": "Streaming Release", "rel_num": 1.0, "country": "GB"},
    {"id": "movie_alien_romulus", "title": "Alien: Romulus", "score": 8.8, "cover": "https://image.tmdb.org/t/p/w500/b33nnKl12oWiICBhZrE2Aoen598.jpg", "genres": ["Horror", "Sci-Fi"], "desc": "While scavenging the deep ends of a derelict space station, young colonizers face the universe's most terrifying life form.", "release": "Theatrical / Digital", "rel_num": 1.0, "country": "US"},
    {"id": "movie_substance", "title": "The Substance", "score": 9.1, "cover": "https://image.tmdb.org/t/p/w500/lqoMzCcZY5yg5y2iM7rQc7f9q2A.jpg", "genres": ["Horror", "Drama", "Sci-Fi"], "desc": "A fading celebrity uses a black-market drug, a cell-replicating substance that creates a younger version of herself.", "release": "MUBI Premiere", "rel_num": 1.0, "country": "FR"}
]

# Curated Fallback Data for All-Time Top Movies
ALL_TIME_MOVIES_GLOBAL = [
    {"id": "movie_shawshank", "title": "The Shawshank Redemption", "score": 9.9, "cover": "https://image.tmdb.org/t/p/w500/9cqNxx0GxF0bflZmeSMuL5tnGzr.jpg", "genres": ["Drama", "Crime"], "desc": "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.", "release": "Masterpiece Edition", "rel_num": 1.0, "country": "US"},
    {"id": "movie_godfather", "title": "The Godfather", "score": 9.8, "cover": "https://image.tmdb.org/t/p/w500/3bhkrj58Vtu7enYsRolD1fZdja1.jpg", "genres": ["Drama", "Crime"], "desc": "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.", "release": "50th Anniversary 4K", "rel_num": 1.0, "country": "US"},
    {"id": "movie_dark_knight", "title": "The Dark Knight", "score": 9.7, "cover": "https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg", "genres": ["Action", "Crime", "Drama"], "desc": "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept his greatest test.", "release": "Trilogy Edition", "rel_num": 1.0, "country": "US"},
    {"id": "movie_lotr_rotk", "title": "The Lord of the Rings: The Return of the King", "score": 9.8, "cover": "https://image.tmdb.org/t/p/w500/rCzpDGLbOoPwLjy3OAm5NUPOTrC.jpg", "genres": ["Adventure", "Fantasy", "Action"], "desc": "Gandalf and Aragorn lead the World of Men against Sauron's army to draw his gaze from Frodo and Sam.", "release": "Extended Edition", "rel_num": 1.0, "country": "NZ"},
    {"id": "movie_pulp_fiction", "title": "Pulp Fiction", "score": 9.6, "cover": "https://image.tmdb.org/t/p/w500/d5iIlFn5s0ImszYzBPb8JPIfbXD.jpg", "genres": ["Crime", "Drama"], "desc": "The lives of two mob hitmen, a boxer, a gangster and his wife intertwine in four tales of violence and redemption.", "release": "Collector's Edition", "rel_num": 1.0, "country": "US"},
    {"id": "movie_fight_club", "title": "Fight Club", "score": 9.5, "cover": "https://image.tmdb.org/t/p/w500/pB8BM7pdSp6B6Ih7QZ4DrQ3PmJK.jpg", "genres": ["Drama", "Psychological"], "desc": "An insomniac office worker and a devil-may-care soap maker form an underground fight club.", "release": "Definitive Remaster", "rel_num": 1.0, "country": "US"},
    {"id": "movie_interstellar", "title": "Interstellar", "score": 9.7, "cover": "https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg", "genres": ["Sci-Fi", "Adventure", "Drama"], "desc": "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.", "release": "10th Anniversary IMAX", "rel_num": 1.0, "country": "US"},
    {"id": "movie_inception", "title": "Inception", "score": 9.6, "cover": "https://image.tmdb.org/t/p/w500/edv5CZvWj09upOsy2Y6IwDhK8bt.jpg", "genres": ["Action", "Sci-Fi", "Adventure"], "desc": "A thief who steals corporate secrets through dream-sharing technology is given the inverse task of planting an idea.", "release": "4K Ultra HD", "rel_num": 1.0, "country": "US"},
    {"id": "movie_parasite", "title": "Parasite", "score": 9.7, "cover": "https://image.tmdb.org/t/p/w500/7IiTTgloJzvGI1TAYymCfbfl3vT.jpg", "genres": ["Comedy", "Thriller", "Drama"], "desc": "Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan.", "release": "Criterion Edition", "rel_num": 1.0, "country": "KR"},
    {"id": "movie_spirited_away", "title": "Spirited Away", "score": 9.7, "cover": "https://image.tmdb.org/t/p/w500/39wmItIWsg5sZMyRUHLkWBcuVCM.jpg", "genres": ["Animation", "Family", "Fantasy"], "desc": "During her family's move to the suburbs, a sullen 10-year-old girl wanders into a world ruled by gods, witches, and spirits.", "release": "Studio Ghibli Fest", "rel_num": 1.0, "country": "JP"}
]

# Country specific TV and Movies datasets
COUNTRY_MEDIA = {
    "kr": {
        "tv": [
            {"id": "tv_squid", "title": "Squid Game: Season 2", "score": 9.5, "cover": "https://image.tmdb.org/t/p/w500/dDlG1TzUgtwHP1jA4e0gX7J6y5I.jpg", "genres": ["Thriller", "Action"], "desc": "Seong Gi-hun re-enters the arena to end the game forever.", "release": "Season 2", "rel_num": 15.0, "country": "KR"},
            {"id": "tv_queen_tears", "title": "Queen of Tears", "score": 9.4, "cover": "https://placehold.co/500x750/1e1b4b/f43f5e?text=Queen+of+Tears", "genres": ["Romance", "Drama"], "desc": "The queen of department stores and the prince of supermarkets weather a marital crisis.", "release": "Episode 16 (Finale)", "rel_num": 16.0, "country": "KR"},
            {"id": "tv_glory", "title": "The Glory", "score": 9.3, "cover": "https://placehold.co/500x750/0a0d14/38bdf8?text=The+Glory", "genres": ["Revenge", "Drama"], "desc": "A woman puts into motion an elaborate revenge plot to make perpetrators pay for horrific school bullying.", "release": "Complete", "rel_num": 16.0, "country": "KR"},
            {"id": "tv_crash_landing", "title": "Crash Landing on You", "score": 9.5, "cover": "https://placehold.co/500x750/111726/6366f1?text=CLOY", "genres": ["Romance", "Comedy"], "desc": "A paragliding mishap drops a South Korean heiress into North Korea - and into the life of an army officer.", "release": "Complete", "rel_num": 16.0, "country": "KR"},
            {"id": "tv_vincenzo", "title": "Vincenzo", "score": 9.2, "cover": "https://placehold.co/500x750/18181b/fbbf24?text=Vincenzo", "genres": ["Action", "Crime", "Comedy"], "desc": "A Korean-Italian mafia lawyer gives an unrivaled conglomerate a taste of its own medicine.", "release": "Complete", "rel_num": 20.0, "country": "KR"},
            {"id": "tv_moving", "title": "Moving", "score": 9.4, "cover": "https://placehold.co/500x750/1e293b/38bdf8?text=Moving", "genres": ["Supernatural", "Action"], "desc": "High school students with hidden superhuman abilities and their parents face dark forces.", "release": "Complete", "rel_num": 20.0, "country": "KR"},
            {"id": "tv_sweet_home", "title": "Sweet Home: Season 3", "score": 8.9, "cover": "https://placehold.co/500x750/18181b/ef4444?text=Sweet+Home", "genres": ["Horror", "Action"], "desc": "Monsters overrun the human world as survivors fight for humanity.", "release": "Season 3 Finale", "rel_num": 26.0, "country": "KR"},
            {"id": "tv_all_of_us_dead", "title": "All of Us Are Dead", "score": 9.1, "cover": "https://placehold.co/500x750/0f172a/10b981?text=All+of+Us+Dead", "genres": ["Zombie", "Horror"], "desc": "A high school becomes ground zero for a zombie virus outbreak.", "release": "Season 2 Upcoming", "rel_num": 12.0, "country": "KR"},
            {"id": "tv_itaewon", "title": "Itaewon Class", "score": 9.2, "cover": "https://placehold.co/500x750/18181b/c084fc?text=Itaewon+Class", "genres": ["Drama", "Inspirational"], "desc": "In a colorful Seoul neighborhood, an ex-con and his friends fight an ambitious foe.", "release": "Complete", "rel_num": 16.0, "country": "KR"},
            {"id": "tv_signal", "title": "Signal", "score": 9.4, "cover": "https://placehold.co/500x750/111726/818cf8?text=Signal", "genres": ["Crime", "Sci-Fi", "Mystery"], "desc": "Detectives from the past and present communicate via a mysterious walkie-talkie to solve cold cases.", "release": "Complete", "rel_num": 16.0, "country": "KR"}
        ],
        "movie": [
            {"id": "movie_parasite", "title": "Parasite", "score": 9.8, "cover": "https://image.tmdb.org/t/p/w500/7IiTTgloJzvGI1TAYymCfbfl3vT.jpg", "genres": ["Thriller", "Drama"], "desc": "Bong Joon-ho's historic 4-time Oscar-winning masterpiece.", "release": "Available on Streaming", "rel_num": 1.0, "country": "KR"},
            {"id": "movie_train_to_busan", "title": "Train to Busan", "score": 9.4, "cover": "https://placehold.co/500x750/18181b/ef4444?text=Train+to+Busan", "genres": ["Action", "Horror"], "desc": "A father and daughter must survive a zombie outbreak aboard a speeding high-speed bullet train.", "release": "Available on Streaming", "rel_num": 1.0, "country": "KR"},
            {"id": "movie_handmaiden", "title": "The Handmaiden", "score": 9.5, "cover": "https://placehold.co/500x750/1e1b4b/38bdf8?text=The+Handmaiden", "genres": ["Romance", "Thriller"], "desc": "Park Chan-wook's visually stunning erotic psychological thriller.", "release": "Criterion Edition", "rel_num": 1.0, "country": "KR"},
            {"id": "movie_oldboy", "title": "Oldboy", "score": 9.6, "cover": "https://placehold.co/500x750/18181b/f43f5e?text=Oldboy", "genres": ["Action", "Mystery"], "desc": "After being kidnapped and imprisoned for fifteen years, Oh Dae-su is released and seeks vengeance.", "release": "4K Restoration", "rel_num": 1.0, "country": "KR"},
            {"id": "movie_exhuma", "title": "Exhuma", "score": 9.3, "cover": "https://placehold.co/500x750/0a0d14/fbbf24?text=Exhuma", "genres": ["Mystery", "Horror"], "desc": "Shamans and a geomancer uncover sinister historical curses while exhuming a cursed tomb.", "release": "Available Now", "rel_num": 1.0, "country": "KR"},
            {"id": "movie_memories_murder", "title": "Memories of Murder", "score": 9.6, "cover": "https://placehold.co/500x750/111726/6366f1?text=Memories+Murder", "genres": ["Crime", "Drama"], "desc": "In 1986, detectives investigate the country's first serial murder cases in a rural province.", "release": "Criterion Edition", "rel_num": 1.0, "country": "KR"},
            {"id": "movie_burning", "title": "Burning", "score": 9.2, "cover": "https://placehold.co/500x750/18181b/f59e0b?text=Burning", "genres": ["Mystery", "Drama"], "desc": "Lee Chang-dong's mesmerizing adaptation of Haruki Murakami's short story.", "release": "Available on Streaming", "rel_num": 1.0, "country": "KR"},
            {"id": "movie_past_lives", "title": "Past Lives", "score": 9.4, "cover": "https://placehold.co/500x750/1e293b/38bdf8?text=Past+Lives", "genres": ["Romance", "Drama"], "desc": "Nora and Hae Sung, two deeply connected childhood friends, are wrest apart after Nora's family emigrates.", "release": "Available to Rent/Buy", "rel_num": 1.0, "country": "KR"},
            {"id": "movie_decision_leave", "title": "Decision to Leave", "score": 9.3, "cover": "https://placehold.co/500x750/0f172a/818cf8?text=Decision+Leave", "genres": ["Mystery", "Romance"], "desc": "A polite detective investigates a man's fatal fall from a mountain peak.", "release": "MUBI Release", "rel_num": 1.0, "country": "KR"},
            {"id": "movie_roundup_punishment", "title": "The Roundup: Punishment", "score": 9.0, "cover": "https://placehold.co/500x750/18181b/10b981?text=The+Roundup", "genres": ["Action", "Crime"], "desc": "Detective Ma Seok-do joins the Cyber Investigation Team to take down an illegal online gambling syndicate.", "release": "Available on Streaming", "rel_num": 1.0, "country": "KR"}
        ]
    },
    "jp": {
        "tv": [
            {"id": "tv_shogun", "title": "Shōgun", "score": 9.6, "cover": "https://image.tmdb.org/t/p/w500/7O4iVfOMQmdCSxhOg1WNzG1AgYT.jpg", "genres": ["Drama", "War & Politics"], "desc": "Lord Toranaga battles for survival in feudal Japan.", "release": "Season 1 Finale", "rel_num": 10.0, "country": "JP"},
            {"id": "tv_alice", "title": "Alice in Borderland", "score": 9.2, "cover": "https://placehold.co/500x750/18181b/ef4444?text=Alice+Borderland", "genres": ["Action", "Sci-Fi"], "desc": "An aimless gamer and his friends find themselves in an empty Tokyo forced to compete in dangerous games.", "release": "Season 3 Upcoming", "rel_num": 16.0, "country": "JP"},
            {"id": "tv_house_ninjas", "title": "House of Ninjas", "score": 8.9, "cover": "https://placehold.co/500x750/0a0d14/6366f1?text=House+Ninjas", "genres": ["Action", "Drama"], "desc": "Years after retiring from their ninja lives, a dysfunctional family must return to shadowy missions.", "release": "Complete", "rel_num": 8.0, "country": "JP"},
            {"id": "tv_first_love", "title": "First Love: Hatsukoi", "score": 9.3, "cover": "https://placehold.co/500x750/111726/38bdf8?text=First+Love", "genres": ["Romance", "Drama"], "desc": "Inspired by songs by Hikaru Utada, a couple retraces their unforgettable first love across decades.", "release": "Complete", "rel_num": 9.0, "country": "JP"},
            {"id": "tv_sanctuary", "title": "Sanctuary", "score": 9.0, "cover": "https://placehold.co/500x750/18181b/fbbf24?text=Sanctuary", "genres": ["Sports", "Drama"], "desc": "A juvenile delinquent becomes a sumo apprentice, shaking an industry steeped in traditions.", "release": "Complete", "rel_num": 8.0, "country": "JP"},
            {"id": "tv_midnight_diner", "title": "Midnight Diner: Tokyo Stories", "score": 9.4, "cover": "https://placehold.co/500x750/1e293b/10b981?text=Midnight+Diner", "genres": ["Food", "Slice of Life"], "desc": "A small Tokyo diner opens from midnight to 7 a.m., warming hearts with soulful recipes and life advice.", "release": "Complete", "rel_num": 30.0, "country": "JP"},
            {"id": "tv_makanai", "title": "The Makanai: Cooking for the Maiko House", "score": 9.1, "cover": "https://placehold.co/500x750/0f172a/c084fc?text=The+Makanai", "genres": ["Drama", "Food"], "desc": "Hirokazu Kore-eda directs this warm, heartwarming tale of two friends in a Kyoto maiko house.", "release": "Complete", "rel_num": 9.0, "country": "JP"},
            {"id": "tv_tokyo_vice", "title": "Tokyo Vice", "score": 9.2, "cover": "https://placehold.co/500x750/18181b/f43f5e?text=Tokyo+Vice", "genres": ["Crime", "Drama"], "desc": "An American journalist descends into the neon-lit underbelly of Tokyo in the late 1990s.", "release": "Season 2 Finale", "rel_num": 18.0, "country": "JP"},
            {"id": "tv_erased_live", "title": "Erased (Live Action)", "score": 8.9, "cover": "https://placehold.co/500x750/111726/818cf8?text=Erased", "genres": ["Mystery", "Thriller"], "desc": "Satoru travels 18 years back in time to prevent a series of kidnappings that claimed lives.", "release": "Complete", "rel_num": 12.0, "country": "JP"},
            {"id": "tv_like_dragon", "title": "Like a Dragon: Yakuza", "score": 8.8, "cover": "https://placehold.co/500x750/18181b/ffffff?text=Yakuza", "genres": ["Action", "Crime"], "desc": "Follow Kazuma Kiryu's brotherhood, rivalry, and devotion in Kamurocho.", "release": "Season 1", "rel_num": 6.0, "country": "JP"}
        ],
        "movie": [
            {"id": "movie_godzilla_minus", "title": "Godzilla Minus One", "score": 9.7, "cover": "https://image.tmdb.org/t/p/w500/hkxxMIGaiCTmrEArK7J56Jv2x8O.jpg", "genres": ["Sci-Fi", "Action"], "desc": "Academy Award winner for Best Visual Effects. Japan faces the King of Monsters.", "release": "Available on Streaming", "rel_num": 1.0, "country": "JP"},
            {"id": "movie_spirited_away", "title": "Spirited Away", "score": 9.8, "cover": "https://image.tmdb.org/t/p/w500/39wmItIWsg5sZMyRUHLkWBcuVCM.jpg", "genres": ["Animation", "Fantasy"], "desc": "Hayao Miyazaki's Oscar-winning fantasy classic about courage and wonder.", "release": "Masterpiece", "rel_num": 1.0, "country": "JP"},
            {"id": "movie_boy_heron", "title": "The Boy and the Heron", "score": 9.5, "cover": "https://placehold.co/500x750/1e1b4b/38bdf8?text=Boy+%26+Heron", "genres": ["Animation", "Fantasy"], "desc": "Hayao Miyazaki's semi-autobiographical Oscar-winning fantasy masterpiece.", "release": "Available on Streaming", "rel_num": 1.0, "country": "JP"},
            {"id": "movie_seven_samurai", "title": "Seven Samurai", "score": 9.9, "cover": "https://placehold.co/500x750/0a0d14/fbbf24?text=Seven+Samurai", "genres": ["Action", "Drama"], "desc": "Akira Kurosawa's monumental cinematic masterpiece that influenced world cinema.", "release": "4K Restoration", "rel_num": 1.0, "country": "JP"},
            {"id": "movie_perfect_days", "title": "Perfect Days", "score": 9.4, "cover": "https://placehold.co/500x750/111726/6366f1?text=Perfect+Days", "genres": ["Drama"], "desc": "Hirayama cleans public toilets in Tokyo, finding immense beauty in daily routines and music.", "release": "Available on Streaming", "rel_num": 1.0, "country": "JP"},
            {"id": "movie_drive_my_car", "title": "Drive My Car", "score": 9.4, "cover": "https://placehold.co/500x750/18181b/f59e0b?text=Drive+My+Car", "genres": ["Drama"], "desc": "Ryusuke Hamaguchi's Academy Award-winning adaptation of Haruki Murakami.", "release": "Available on Streaming", "rel_num": 1.0, "country": "JP"},
            {"id": "movie_your_name", "title": "Your Name (Kimi no Na wa)", "score": 9.6, "cover": "https://placehold.co/500x750/18181b/38bdf8?text=Your+Name", "genres": ["Animation", "Romance"], "desc": "Two teenagers share a profound connection upon discovering they are swapping bodies across time.", "release": "Available on Streaming", "rel_num": 1.0, "country": "JP"},
            {"id": "movie_monster_koreeda", "title": "Monster", "score": 9.3, "cover": "https://placehold.co/500x750/1e293b/ef4444?text=Monster", "genres": ["Mystery", "Drama"], "desc": "When her young son begins behaving strangely, a mother confronts his teacher with profound surprises.", "release": "Available on Streaming", "rel_num": 1.0, "country": "JP"},
            {"id": "movie_harakiri", "title": "Harakiri", "score": 9.7, "cover": "https://placehold.co/500x750/0f172a/818cf8?text=Harakiri", "genres": ["Drama", "Action"], "desc": "An elder ronin arrives at the gate of a clan requesting to commit seppuku in their courtyard.", "release": "Criterion Edition", "rel_num": 1.0, "country": "JP"},
            {"id": "movie_ran", "title": "Ran", "score": 9.6, "cover": "https://placehold.co/500x750/18181b/ffffff?text=Ran", "genres": ["War", "Drama"], "desc": "Akira Kurosawa's visual epic transposing King Lear to Sengoku-era warlord domains.", "release": "4K Ultra HD", "rel_num": 1.0, "country": "JP"}
        ]
    }
}

def to_media_item(raw: dict, media_type: MediaType, rank: Optional[int] = None) -> MediaItem:
    title = raw["title"]
    providers = generate_provider_links(media_type, title, original_id=raw["id"])
    return MediaItem(
        id=f"tmdb_{raw['id']}",
        source="tmdb",
        mediaType=media_type,
        title=title,
        coverImage=raw["cover"],
        description=raw["desc"],
        genres=raw["genres"],
        status="ongoing" if media_type == MediaType.TV else "completed",
        latestRelease=raw["release"],
        latestReleaseNumber=raw["rel_num"],
        officialProviders=providers,
        score=raw["score"],
        rank=rank,
        country=raw.get("country", "US")
    )

async def search_tmdb(query: str, media_type: str = "tv") -> List[MediaItem]:
    cache_key = f"tmdb_search_{media_type}_{query.lower()}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    results: List[MediaItem] = []
    
    # 1. If TMDB API key is configured, query TMDB search endpoint
    if settings.TMDB_API_KEY:
        try:
            endpoint = "search/tv" if media_type == "tv" else "search/movie"
            url = f"{settings.TMDB_BASE_URL}/{endpoint}"
            params = {
                "query": query,
                "include_adult": "false"
            }
            headers = {}
            if settings.TMDB_API_KEY.startswith("eyJ"):
                headers["Authorization"] = f"Bearer {settings.TMDB_API_KEY}"
            else:
                params["api_key"] = settings.TMDB_API_KEY

            async with httpx.AsyncClient(timeout=8.0) as client:
                resp = await client.get(url, params=params, headers=headers)
                if resp.status_code == 200:
                    data = resp.json().get("results", [])
                    m_type = MediaType.TV if media_type == "tv" else MediaType.MOVIE
                    for item in data[:10]:
                        title = item.get("name") if media_type == "tv" else item.get("title")
                        if not title:
                            continue
                        poster = item.get("poster_path")
                        cover = f"https://image.tmdb.org/t/p/w500{poster}" if poster else "https://placehold.co/500x750/18181b/ffffff?text=No+Cover"
                        vote = float(item.get("vote_average", 8.0))
                        overview = item.get("overview", "")
                        origin = item.get("origin_country", ["US"])[0] if item.get("origin_country") else "US"
                        providers = generate_provider_links(m_type, title, original_id=f"tmdb_{item.get('id')}")

                        results.append(MediaItem(
                            id=f"tmdb_{media_type}_{item.get('id')}",
                            source="tmdb",
                            mediaType=m_type,
                            title=title,
                            originalTitle=item.get("original_name") or item.get("original_title"),
                            coverImage=cover,
                            description=overview[:390] + "..." if len(overview) > 390 else overview,
                            genres=["Entertainment", "Drama"],
                            status="ongoing" if media_type == "tv" else "completed",
                            latestRelease="Available on TMDb",
                            latestReleaseNumber=1.0,
                            officialProviders=providers,
                            score=vote,
                            country=origin
                        ))
        except Exception as exc:
            print(f"TMDB API query error: {exc}")

    # 2. If TV search and no TMDB results, use free TVMaze live API (Zero API key required)
    if media_type == "tv" and len(results) < 5:
        try:
            tvmaze_url = f"https://api.tvmaze.com/search/shows?q={query}"
            async with httpx.AsyncClient(timeout=6.0) as client:
                resp = await client.get(tvmaze_url)
                if resp.status_code == 200:
                    shows_data = resp.json()
                    for entry in shows_data[:8]:
                        show = entry.get("show") or {}
                        name = show.get("name")
                        if not name or any(r.title.lower() == name.lower() for r in results):
                            continue

                        img_dict = show.get("image") or {}
                        cover = img_dict.get("medium") or img_dict.get("original") or "https://placehold.co/500x750/18181b/ffffff?text=TV+Show"
                        
                        summary = show.get("summary") or ""
                        # Strip basic html tags
                        for tag in ("<p>", "</p>", "<b>", "</b>", "<i>", "</i>", "<br>"):
                            summary = summary.replace(tag, "")

                        rating_avg = (show.get("rating") or {}).get("average")
                        score = float(rating_avg) if rating_avg else 8.5
                        genres = show.get("genres") or ["Drama", "TV Series"]
                        status = "ongoing" if show.get("status") == "Running" else "completed"
                        premiered = show.get("premiered") or ""
                        latest_rel = f"Premiered {premiered}" if premiered else "Airing"
                        
                        country_code = ((show.get("network") or {}).get("country") or {}).get("code", "US")
                        providers = generate_provider_links(MediaType.TV, name, original_id=f"tv_{show.get('id')}")

                        results.append(MediaItem(
                            id=f"tvmaze_{show.get('id')}",
                            source="tvmaze",
                            mediaType=MediaType.TV,
                            title=name,
                            coverImage=cover,
                            description=summary[:390] + "..." if len(summary) > 390 else summary,
                            genres=genres,
                            status=status,
                            latestRelease=latest_rel,
                            latestReleaseNumber=1.0,
                            officialProviders=providers,
                            score=score,
                            country=country_code
                        ))
        except Exception as exc:
            print(f"TVMaze fallback error: {exc}")

    # 3. Fallback to matching curated
    if len(results) < 5:
        m_type = MediaType.TV if media_type == "tv" else MediaType.MOVIE
        pool = (TRENDING_TV_GLOBAL + ALL_TIME_TV_GLOBAL) if media_type == "tv" else (TRENDING_MOVIES_GLOBAL + ALL_TIME_MOVIES_GLOBAL)
        q_lower = query.lower()
        for c in pool:
            if q_lower in c["title"].lower():
                if not any(r.title.lower() == c["title"].lower() for r in results):
                    results.append(to_media_item(c, m_type))

    cache.set(cache_key, results, ttl=60)
    return results

async def get_popular_tmdb(media_type: str = "tv", limit: int = 10) -> List[MediaItem]:
    return await get_top_tmdb(media_type=media_type, mode="trending", limit=limit)

async def get_top_tmdb(media_type: str = "tv", mode: str = "trending", country: str = "global", limit: int = 10) -> List[MediaItem]:
    cache_key = f"tmdb_top_{media_type}_{mode}_{country.lower()}_{limit}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    c_lower = country.lower()
    m_type = MediaType.TV if media_type == "tv" else MediaType.MOVIE

    # Check country-specific curated
    if c_lower in COUNTRY_MEDIA and media_type in COUNTRY_MEDIA[c_lower]:
        items = COUNTRY_MEDIA[c_lower][media_type]
    elif media_type == "tv":
        items = ALL_TIME_TV_GLOBAL if mode == "top_rated" else TRENDING_TV_GLOBAL
    else:
        items = ALL_TIME_MOVIES_GLOBAL if mode == "top_rated" else TRENDING_MOVIES_GLOBAL

    results = [to_media_item(item, m_type, rank=idx + 1) for idx, item in enumerate(items[:limit])]
    cache.set(cache_key, results, ttl=60)
    return results
