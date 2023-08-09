from iterations.utils import *
from datetime import datetime
from termcolor import cprint, colored

# print banner
banner = """                                                                                                                
                                                                                                                         
                                                                                      .    .!YGY                         
                                                                                    ^BP      ^@B                         
                              :!!!!^~:  ^7J! ^77^    ^!!77^   .^7?^     !^    :!: ::7@P:::    #G :~7?!.                  
                            :PG!::~B@! ^!!#@J!?#J  7BY~^^?&B^ ~~!&&:  .5@B    7@P ~~J@P~!^    ##77!7P@5           ~^     
                           .#&.    P@^    5@^  .  ~@P     7@G    J@7 :Y^J@!   .&?   ~@Y      .#G    .&G      .^75#@J     
                           !@G     P@^    5@:     J@Y     ~@B    ^@Y^5: .&#. .Y7    ~@Y      .&P    .&G   :7YB@@@@@J     
                           :&@?. .^G@^    G@:     ^&@~   .P@!    .&@5.   7@5!J^     ~@B:.^^  :@P    :@#::~.  ?@@@B@P     
                     :~~.   ^NVDA?!B@:    55.      ^5GY??YJ^      Y5.     5P~       .YBPJ!.  :G7     Y#P?^  7@@@? ^J.    
                  ~AI&@@#?        ^@P        :7??7    ...               .^?J            .^J?...            7@@@Y         
               :J#@@#@@@@5  YB7^~7PJ.        G@@@@P.            ..:~!?5B&@#P^   ..^~7JPB&@#G##&BY~.       ~@@@B          
            .7G@&5!^5@@@5   .~7!~^.    ^~^~7GROWTH@#7        YBBSTOCKS5J!^.  PBB##BBBG5J!:  7@@@@@#5~     B@@@!          
          ^5&#5~. ^G@@@J            ~5B@@@B57^^P@@@@@B7.     ^!&@B~?7        ^?@@G7~         ?@@@&@@@G!  !@@@B           
       .7B&P!.  .J@@@&7           ^G@@@BJ^.    :&@@5Y&@&Y^    J#@@&G? .^!?YPGGG&@@&7  .^7J5NET@@@B~Y&@@P:5@@@?           
     :J##J:     AMZN?:     ..:::.^&@@&?         J@@B .~JB@BJ^ !?&@@?JB&@#GY7~^.!@@&?5B&@#PY7~^?#@7  :P@@&&@@@^           
   .Y&G!       ..:^~!7JY5PPPGPPP5P@@@P      :   ^@@@^    5@@@B^ #@@@@G?^.      :@@@@@P7^       .^     7&@@@@#.           
  ~#@5^^~!?Y5GGBGPP5YY?~^::..    ~@@@@!   ^5@5   #@@CRWD#PLTRJ: ?JYJ:          .?JY?:                  :^~!??            
 ~@@@@@@@&ELF?~:. ~J#&&G~      .J&@@@@@#B#@@#J   B@@7:#@@G                                                               
 :JYJ?7~:.          J@@@#    .?#@@#J^7J55Y?~.   .#@@! ^&@@P                                                              
                    !@@@B  :Y&@@G7.              J5P^  ~#@@G:                                                            
                    P@@@7~P@@BJ^                        :P@@&7                                                           
                   ?@@@&#@#Y~                             7#@@G~                                                         
                  ^&@@@GJ^                                 .7G@@B?:                                                      
                   .^!~                                       :7YP57^                                                    
                                                                              
"""
cprint(banner, "cyan")

time = datetime.now()
cprint("" + time.strftime("%m/%d/%Y %H:%M:%S"))

# run screen iterations
import iterations.nasdaq_listings
import iterations.relative_strength

# import iterations.liquidity
# import iterations.trend
# import iterations.revenue_growth
# import iterations.institutional_accumulation


# # open screen results as a DataFrame
# final_iteration = "institutional_accumulation"
# df = open_outfile(final_iteration)


time_string = time.strftime("%Y-%m-%d %H-%M-%S")

# # create a .csv outfile
# outfile_name = f"screen_results {time_string}.csv"
# df.to_csv(outfile_name)

# print(f"\nDONE! (created {outfile_name})")
