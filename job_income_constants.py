# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 18:16:04 2016

@author: dhartig
"""

metro_splits = {}
                
metro_splits_csa = {45940: [35614, 37964], # Trenton: NYC, Philly
                75700: [35614, 73450], # New Haven: NYC, Hartford
                10900: [35614, 37964], # Allentown: NYC, Philly
                44700: [41884, 40900], # Stockton: San Fran, Sacramento
                29460: [36740, 45300], # Lakeland: Orlando, Tampa
                27500: [31540, 40420] # Janesville: Madison, Rockford
                }

id_map = {  35614: [35084, 35004, 20524, 71950], #NYC
            31084: [11244], #LA
            16974: [20994, 23844, 29404], #Chicago
            47894: [43524], #DC
            41884: [36084, 42034], # San Fran, San Jose, Vallejo, Santa Rosa, Santa Cruz, Napa
            71654: [72104, 73104, 73604, 74204, 74804, 74854, 76524, 78254, 76900, 73050], #Boston, Brockton, Framingham, Haverhill, Lawrence, Lowell, Lynn, Peabody, Taunton, Portsmouth, Dover
            79600: [74500], #Worcester, Leominster
            77200: [75550], #Providence, New Bedford
            74950: [75404], #Manchester, Nashua 
            19124: [23104], # Dallas, Fort Worth  , Sherman          
            37964: [33874, 15804, 48864], #Philadelphia, Montogmery, Camden, Wilmington
            33124: [22744, 48424], # Miami, Ft. Lauderdale, West Palm Beach
            19804: [47664], # Detroit, Warren
            42644: [45104]} #Seattle, Tacoma


id_map_csa = {  35614: [35084, 35004, 20524, 71950, 28740, 20700], #NYC, Fairfield, Kingston, East Stroudsburg
            31084: [11244, 40140, 37100], #LA, Orange, Riverside, Oxnard
            16974: [20994, 23844, 29404, 28100], #Chicago, Kankakee
            47894: [43524, 12580, 25180, 16540, 49020, 15680], #DC, Baltimore, Hagerstown, Chambersberg, Winchester, California
            41884: [36084, 42034, 41940, 46700, 42220, 42100, 34900], # San Fran, San Jose, Vallejo, Santa Rosa, Santa Cruz, Napa
            71654: [72104, 73104, 73604, 74204, 74804, 74854, 76524, 78254, 75404, 76900, 73050, 79600, 74500, 77200, 75550, 74950, 70900], #Boston, Brockton, Framingham, Haverhill, Lawrence, Lowell, Lynn, Peabody, Taunton, Nashua, Portsmouth, Dover, Worcester, Leominster, Providence, New Bedford, Manchester, Barnstable
            19124: [23104, 43300], # Dallas, Fort Worth  , Sherman          
            37964: [33874, 15804, 48864, 47220, 39740, 12100, 20100, 36140], #Philadelphia, Montogmery, Camden, Wilmington, Vineland, Reading, Atlantic City, Dover, Ocean City
            33124: [22744, 48424, 38940, 42680], # Miami, Ft. Lauderdale, West Palm Beach, Port St. Lucie, Sebastian
            12060: [12020, 23580], #Atlanta, Athens, Gainesville
            19804: [47664, 11460, 22420, 33780], # Detroit, Warren, Ann Arbor, Flint, Monroe
            42644: [45104, 36500, 17740, 34580], #Seattle, Tacoma, Olympia, Bremerton, Mount Vernon
            33460: [41060], #Minneapolis, St. Cloud
            17460: [10420, 15940, 49660], #Cleveland, Akron, Canton, Youngstown
            19740: [14500, 24540, 22660], #Denver, Boulder, Greely, Ft. Collins
            38900: [41420, 10540, 31020, 18700], # Portland, Salem, Albany, Longview, Corvallis
            36740: [19660, 45540, 37340], # Orlando, Deltona, The Villages, Palm Bay
            45300: [35840], # Tampa, North Port
            38300: [48260, 48540], #Pittsburgh, Wierton, Wheeling
            40900: [49700], #Sacramento, Yuba City
            41620: [39340, 36260], # Salt Lake City, Provo, Ogden
            28140: [41140, 29940],  # Kansas City, St. Joseph, Lawrence
            26900: [34620, 18020, 14020], #Indianapolis, Muncie, Columbus, Bloomington
            29820: [29420], #Las Vegas, Lake Havasu City
            39580: [20500], # Raleigh, Durham
            33340: [39540], # Milwaukee, Racine
            73450: [78100, 76450], #Hartford, Springfield, Norwich
            25420: [49620, 23900, 30140, 29540], #Harrisburg, York, Gettysburg, Lebanon, Lancaster
            24660: [49180, 72400], # Greensboro, Winston-Salem, Burlington
            31140: [21060], #Louisville, Elizabethtown
            35380: [25220, 26380], #New Orleans, Hammond, Houma
            24340: [34740], # Grand Rapids, Muskegon
            24860: [43900], # Greenville, Spartanburg    
            10580: [24020], #Albany, Glens Falls
            10740: [42140], #Albuquerque, Santa Fe
            23420: [31460], #Fresno, Madera
            28940: [34100], #Knoxville, Morristown
            19380: [44220], #Dayton, Springfield
            21340: [29740], #El Paso, Las Cruces
            15980: [34940, 39460], # Cape Coral, Naples, Punta Gorda
            16860: [19140, 17420], # Chattanooga, Dalton, Cleveland
            30780: [38220, 26300], #Little Rock, Pine Bluff, Hot Springs
            33700: [32900], #Modesto, Merced
            19780: [11180], #Des Moines, Ames
            43780: [21140, 35660], #South Bend, Elkhart, Niles
            26580: [16620], # Huntington, Charleston
            26620: [19460], #Huntsville, Decatur
            44060: [17660], #Spokane, Couer d'Alene
            76750: [74650], #Portland, Lewiston
            33660: [19300, 37860], #Mobile, Daphne, Pensacola
            47300: [25260], # Visalia, Hanford
            27740: [28700], #Johnson City, Kingsport
            37900: [14010], #Peoria, Bloomington
            24580: [11540, 36780], #Green Bay, Appleton, Oshkosh
}

cost_of_living = {35614: 81.77, 35084: 81.77, 35004: 81.77, 20524: 81.77, 71950: 83.06, 45940: 88.89, 75700: 88.57, 10900: 99.70, 28740: 96.99, 20700: 101.2, #NYC, Newark, Nassau, Dutchess, Fairfield, Trenton, New Haven, Allentown, Kingston, East Stroudsburg
                  31084: 85.47, 11244: 85.47, 40140: 94.43, 37100: 87.18,  #LA, Orange, Riverside, Oxnard
                  16974: 94.34, 20994: 94.34, 23844: 94.34, 29404: 94.34, 28100: 101.00, #Chicago, Elgin, Gary, Lake, Kankakee
                  47894: 83.75, 43524: 83.75, 12580: 92.59, 25180: 98.14, 16540: 106.3, 49020: 109.5, 15680: 101.8, # Washington, Silver Spring, Baltimore, Hagerstown, Chambersberg, Winchester, California
                  41884: 82.44, 36084: 82.44, 42034: 82.44, 41940: 81.37, 46700: 86.66, 44700: 99.6, 42220: 84.53, 42100: 82.1, 34900: 84.1, # San Fran, Oakland, San Rafael, San Jose, Vallejo, Stockton, Santa Rosa, Santa Cruz, Napa
                  71654: 90.66, 72104: 90.66, 73104: 90.66, 73604: 90.66, 74204: 90.66, 74804: 90.66, 74854: 90.66, 76524: 90.66, 78254: 90.66, 75404: 92.42, 76900: 90.66, 73050: 90.66, #Boston, Brockton, Framingham, Haverhill, Lawrence, Lowell, Lynn, Peabody, Taunton, Nashua, Portsmouth, Dover
                                      79600: 96.25, 74500: 96.25, 77200: 101.0, 75550: 101.0, 74950: 92.42, 70900: 98.14, #Worcester, Leominster, Providence, New Bedford, Manchester, Barnstable
                  19124: 99.6, 23104: 99.6, 43300: 109.5, #Dallas, Fort Worth, Sherman
                  37964: 93.28, 33874: 93.28, 15804: 93.28, 48864: 93.28, 47220: 97.85, 39740: 104.2, 12100: 93.46, 20100: 106.20, 36140: 93.28, #Philadelphia, Montogmery, Camden, Wilmington, Vineland, Reading, Atlantic City, Dover, Ocean City
                  26420: 99.70, # Houston
                  33124: 94.43, 22744: 94.43, 48424: 94.43, 38940: 104.4, 42680: 110.0, # Miami, Ft. Lauderdale, West Palm Beach, Port St. Lucie, Sebastian
                  12060: 104.6, 12020: 108.7, 23580: 112.4, #Atlanta, Athens, Gainesville
                  19804: 102.8, 47664: 102.8, 11460: 98.04, 22420: 107.8, 33780: 104.8, # Detroit, Warren, Ann Arbor, Flint, Monroe
                  42644: 92.76, 45104: 92.76, 36500: 94.88, 17740: 95.24, 34580: 102.8, #Seattle, Tacoma, Olympia, Bremerton, Mount Vernon
                  38060: 102.4, #Phoenix
                  33460: 97.47, 41060: 107.0, #Minneapolis, St. Cloud
                  17460: 112.2, 10420: 112.6, 15940: 112.0, 49660: 112.6, #Cleveland, Akron, Canton, Youngstown
                  19740: 95.51, 14500: 91.66, 24540: 101.1, 22660: 98.62, #Denver, Boulder, Greely, Ft. Collins
                  41740: 86.28, #San Diego
                  38900: 98.72, 41420: 104.8, 10540: 106.4, 31020: 107.0, 18700: 101.4, # Portland, Salem, Albany, Longview, Corvallis
                  36740: 102.2, 29460: 107.2, 19660: 104.5, 45540: 110.9, 37340: 105.0,# Orlando, Lakeland, Deltona, The Villages, Palm Bay
                  45300: 99.0, 35840: 101.3, # Tampa, North Port
                  41180: 110.5, # St. Louis
                  38300: 105.5, 48260: 114.8, 48540: 115.3, #Pittsburgh, Wierton, Wheeling
                  16740: 106.8, #Charlotte
                  40900: 97.56, 49700: 101.5, #Sacramento, Yuba City
                  41620: 100.3, 39340: 102.8, 36260: 104.3, # Salt Lake City, Provo, Ogden
                  28140: 107.1, 41140: 112.5, 29940: 106.0, # Kansas City, St. Joseph, Lawrence
                  18140: 107.1, #Columbus
                  26900: 107.1, 34620: 111.6, 18020: 114.0, 14020: 105.4, #Indianapolis, Muncie, Columbus, Bloomington
                  41700: 105.9, # San Antonio
                  29820: 101.3, 29420: 106.8, # Las Vegas, Lake Havasu
                  17140: 111.4, #Cincinnati
                  39580: 104.3, 20500: 104.8, #Raleigh, Durham
                  33340: 104.3, 39540: 106.4, #Milwaukee, Racine
                  12420: 101.0, # Austin
                  34980: 106.5, # Nashville
                  47260: 101.6, # Virginia Beach
                  73450: 99.3, 78100: 103.3, 76450: 99.5, #Hartford, Springfield, Norwich
                  25420: 104.2, 49620: 104.1, 23900: 104.6, 30140: 105.4, 29540: 101.6, #Harrisburg, York, Gettysburg, Lebanon, Lancaster
                  24660: 110.7, 49180: 111.1, 72400: 110.5 , # Greensboro, Winston-Salem, Burlington 
                  27260: 104.2, #Jacksonville
                  31140: 109.4, 21060: 116.3, #Louisville, Elizabethtown
                  35380: 104.2, 25220: 117.2, 26380: 107.5, #New Orleans, Hammond, Houma
                  24340: 106.7, 34740: 112.7, # Grand Rapids, Muskegon
                  24860: 110.9, 43900: 113.9, # Greenville, Spartanburg
                  36420: 108.2, #Oklahoma City
                  32820: 108.8, #Memphis
                  13820: 111.2, #Birmingham
                  40060: 104.0, #Richmond
                  15380: 106.6, #Buffalo
                  40380: 102.7, #Rochester
                  10580: 100.8, 24020: 103.3, #Albany, Glens Falls
                  10740: 102.9, 42140: 100.3, #Albuquerque, Santa Fe     
                  46140: 109.5, #Tulsa
                  23420: 102.8, 31460: 103.3, #Fresno, Madera
                  28940: 110.5, 34100: 122.1, #Knoxville, Morristown
                  19380: 110.0, 44220: 113.0, #Dayton, Springfield
                  46060: 103.0, #Tucson
                  21340: 110.9, 29740: 107.6, #El Paso, Las Cruces
                  15980: 105.2, 34940: 100.04, 39460: 105, # Cape Coral, Naples, Punta Gorda
                  46520: 80.97, #Honolulu
                  16860: 110.4, 19140: 119.2, 17420: 118.9, # Chattanooga, Dalton, Cleveland
                  36540: 106.3, #Omaha
                  17900: 108.8, #Columbia
                  30780: 110.3, 38220: 118.2, 26300: 117.4, #Little Rock, Pine Bluff, Hot Springs
                  32580: 116.7, #McAllen
                  12540: 102.2, #Bakersfield
                  31540: 102.2, 27500: 108.1, #Madison, Beloit
                  12940: 107.2, #Baton Rouge
                  33700: 101.3, 32900: 104.7, #Modesto, Merced
                  19780: 105.4, 11180: 110.9, #Des Moines, Ames
                  14260: 105.2, #Boise
                  45060: 104.7, #Syracuse
                  16700: 103.8, #Charleston
                  43780: 110.9, 21140: 109.9, 35660: 112.1, #South Bend, Elkhart, Niles
                  26580: 115.2, 16620: 112.4, # Huntington, Charleston
                  26620: 110.3, 19460: 114.8, #Huntsville, Decatur
                  44060: 104.6, 17660: 107.6, #Spokane, Couer d'Alene
                  17820: 100.3, # Colorado Springs
                  48620: 109.9, #Wichita
                  27140: 110.4, #Jackson
                  45780: 111.6, # Toledo
                  76750: 99.3, 74650: 105.6, #Portland, Lewiston
                  33660: 112.9, 19300: 108.6, 37860: 107.0, #Mobile, Daphne, Pensacola
                  47300: 104.8, 25260: 107.8, # Visalia, Hanford
                  12260: 112.0, #Augusta
                  42540: 108.9, #Scranton
                  27740: 112.9, 28700: 115.6, #Johnson City, Kingsport  
                  40420: 109.5, # Rockford
                  37900: 108.9, 14010: 106.3, #Peoria, Bloomington
                  24580: 108.7, 11540: 107.9, 36780: 108.9, #Green Bay, Appleton, Oshkosh
                  22220: 111.0, #Fayetteville, AR-MO
                  30460: 108.2, # Lexington
                  29180: 112.2, # Lafayette
                  29620: 106.5, #Lansing
                  44180: 113.0, #Springfield, MO
                  18580: 107.0, #Corpus Christi
                  39900: 100.9, #Reno
                  11700: 107.3, #Asheville
                  42200: 91.91, #Santa Maria
                  43340: 110.0, #Shreveport
                  34820: 109.8, #myrtle Beach
                  28660: 108.0, #Killeen
                  23060: 110.3, #Fort Wayne
                  15180: 117.6, #Brownsville
                  13140: 110.7, #Beaumont
                  #Anchorage
                  
                  
                  
                  
}

occupation_full_code = {'Computer Development': ['15-1111', '15-1143', '15-1131', '15-1132', '15-1133', '15-1143', '17-2061', '25-1021'],
                        'Biotech': ['17-2031', '19-1021', '19-1022', '19-1029', '19-1041', '19-1042', '19-1099', '25-1042'],
                        'Chemistry and Materials': ['17-2041', '17-2131', '19-2031', '19-2032', '25-1052'],
                        'Mathematics and Economics': ['15-2011', '15-2021', '15-2031', '15-2041', '15-2099', '19-3011', '25-1022', '25-1063'],
                        'Physical Science and Energy': ['11-9121',  '17-1021', '17-2081', '17-2151', '17-2161', '17-2171', '19-2011', '19-2012', '19-2021', '19-2041', '19-2042', '19-2043', '19-2099', '25-1051', '25-1054',
                                                        '11-9013', '17-2021', '19-1011', '19-1012', '19-1013', '19-1023', '19-1031', '19-1032', '25-1041'],
                        'Engineering and Industrial': ['11-3051', '11-9041', '17-2011', '17-2051', '17-2071', '17-2072', '17-2111', '17-2112', '17-2121', '17-2041', '17-2199', '41-4011', '41-9031'],
                        'Law': ['23-1011', '23-1012', '23-1021', '23-1022', '23-1023', '25-1112'],
                        'Medicine': ['11-9111', '25-1071', '25-1072', '29-1021', '19-1022', '29-1023', '29-1029', '29-1041', '29-1051', '29-1061', '29-1062', '29-1063', '29-1064', '29-1065', '29-1067', '29-1069', '29-1071', '29-1081', '29-1122', '29-1023', '29-1024', '29-1127',
                                     '29-1141', '29-1151', '29-1161', '29-1181'],
                        'Finance and Accounting': ['11-3031', '13-2011', '13-2031', '13-2041', '13-2051', '13-2052', '13-2053', '13-2031', '13-2072', '13-2081', '13-2099', '41-3031'],
                        'Entertainment and Media': ['25-1121', '27-0000'],
                        'Computer Support': ['11-3021', '15-1121', '15-1122', '15-1134', '15-1141', '15-1142', '15-1152', '15-1199'],
                        'Management and Business': ['11-1011', '11-1021', '11-2011', '11-2021', '11-2022', '11-2031', '11-3011', '11-3061', '11-3071', '11-3111', '11-3121', '11-3131', '11-9199', '13-1011', '13-1111', '25-1011']
                        }





















