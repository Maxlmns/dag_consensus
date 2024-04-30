from simulation.blockchain_initialisation import initialize_blockchain
from simulation.draw_blockchain import DrawBlockchain
from simulation.random_transaction import generate_random_transaction
from simulation.random_user import generate_random_user
from common.reputation import load_user_reputations,save_user_reputations
from common.utils import get_block_credit,is_valid_block,find_block,get_all_credit,get_max_credit,get_total_credit,load_blockchain_dag,get_user_credit,get_user_proportion,validate_all_blocks
from time import time,sleep
from scipy.optimize import minimize

#generate_random_user(30)

initialize_blockchain()
generate_random_transaction(500)
def objective(params):
        alpha, beta, gamma = params
        credit = get_all_credit(alpha, beta, gamma, start_time,end_time)
        total_credit = get_total_credit(credit)
        max_credit = get_max_credit(credit)

        return max(0,1/(max_credit - total_credit/3))   

constraints = ({'type': 'ineq', 'fun': lambda x: x[0]},  # alpha > 0
               {'type': 'ineq', 'fun': lambda x: -x[1]}, # beta < 0
               {'type': 'ineq', 'fun': lambda x: x[2]-1}, # gamma > 1
               {'type': 'ineq', 'fun': lambda x: 100-x[0]},
               {'type': 'ineq', 'fun': lambda x: x[1]+100}
               ) 
initial_guess = [10, -10, 2]
for k in range(20):
    
    

    print(k)
    end_time = time()   

    for j in range(120):
        generate_random_transaction(12)
        sleep(1)
    period = 300
    start_time = end_time-period
    result = minimize(objective, initial_guess, constraints=constraints)
    alpha_opt, beta_opt, gamma_opt = result.x
    print(f"Time: {start_time,end_time}")
    print(f"Optimal alpha: {alpha_opt}")
    print(f"Optimal beta: {beta_opt}")
    print(f"Optimal gamma: {gamma_opt}")
    total_credit = get_total_credit(get_all_credit(alpha_opt, beta_opt, gamma_opt, start_time,end_time))
    max_credit = get_max_credit(get_all_credit(alpha_opt, beta_opt, gamma_opt, start_time,end_time))
    print(f"Total credit: {total_credit}")
    print(f"Max credit: {max_credit}")
    initial_guess = [alpha_opt, beta_opt, gamma_opt]
    
DrawBlockchain()
