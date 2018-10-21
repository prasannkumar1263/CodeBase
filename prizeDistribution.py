from math import log10, floor, ceil


# This is just a function to prettify and print out the prize distribution table

def pretty_print(list1, list2):
    rank_start, rank_end = 0, 0
    for i in range(len(list1)):
        rank_start, rank_end = rank_end+1, rank_end+list1[i]
        if rank_start == rank_end:
            print("{}".format(rankStart), list2[i], sep="    ")
        else:
            print("{}-{}".format(rankStart, rankEnd), list2[i], sep="    ")

# This function will be used to round down numbers to the nearest nice number as defined
# in the research paper


def round_to_nice(number):
    exp_count = 0
    while number > 1000 or number % 10 == 0 and number != 0:
        number = number//10
        exp_count += 1
    if 10 <= number < 100:
        number = (number//5)*5
    elif 250 > number >= 100:
        number = (number//25)*25
    elif 100 > number >= 250:
        number = (number//125)*125
    number = number*(10**exp_count)
    return number

# Used to calculate the sum of the power series


def pow_sum(number_winners, m, entry_fee, excess, bucket_size_list):
    full_sum = 0
    index = 0
    count = bucket_size_list[0]
    bucketed_prize_list = [entry_fee*i for i in bucket_size_list]

    for i in range(1, number_winners+1):
        value = i**(-1*m)
        full_sum += value
        bucketed_prize_list[index] += excess*value
        count -= 1
        if count == 0:
            bucketed_prize_list[index] /= bucket_size_list[index]
            index += 1
            try:
                count = bucket_size_list[index]
            except IndexError:
                break
    return full_sum, bucketed_prize_list

# Function to calculate all the distinct numbers


def calculate_prizes(pot_size, entry_fee, number_winners, p1, bucket_size_list):
    list_items = []
    low, high = 0, 8
    excess = p1-entry_fee
    distribution_ratio = (pot_size-number_winners*entry_fee)/excess
    while low <= high:
        mid = (high+low)/2
        value, list_items = pow_sum(number_winners, mid, entry_fee, excess, bucket_size_list)
        if value < 0.9999*distribution_ratio:
            high = mid
        elif value > 1.0001*distribution_ratio:
            low = mid
        else:
            break
    return list_items

# Calculate the number of winners in each bucket


def calculate_bucket_sizes(number_winners, r_max):
    single_buckets = min(ceil(log10(number_winners))+1, 3)
    bucket_sizes = [1 for _ in range(single_buckets)]
    bucket_sizes.extend([0 for _ in range(r_max-single_buckets)])
    low, high = 1, 100
    mid = 0
    r_max -= single_buckets
    number_winners -= single_buckets
    if r_max != 0:
        while low <= high:
            mid = (high+low)/2
            value = mid*(mid**r_max-1)/(mid-1)
            if value < 0.99*number_winners:
                low = mid
            elif value > 1.01*number_winners:
                high = mid
            else:
                break
        r_max += single_buckets
        number_winners += single_buckets
        for i in range(single_buckets, r_max):
            element_sum = sum(bucket_sizes)
            if ceil(mid * bucket_sizes[i-1])+element_sum <= number_winners:
                if ceil((mid**2)*bucket_sizes[i-1])+ceil(mid*bucket_sizes[i-1])+element_sum > number_winners:
                    bucket_sizes[i] = floor((number_winners-element_sum)/2)
                    bucket_sizes[i+1] = ceil((number_winners-element_sum)/2)
                    break
            bucket_sizes[i] = ceil(mid*bucket_sizes[i-1])
        while bucket_sizes[-1] == 0:
            bucket_sizes.pop(-1)
        bucket_sizes[-1] = 0
        for i in range(len(bucket_sizes)-1):
            bucket_sizes[i] = round_to_nice(bucket_sizes[i])
        bucket_sizes[-1] = number_winners-sum(bucket_sizes)
        return bucket_sizes

# Makes all the prizes as nice numbers


def nice_numerator(pot_size, bucket_size_list, bucket_prize_list):
    excess = 0
    for i in range(len(bucket_size_list)):
        nice_no = round_to_nice(int(bucket_prize_list[i]))
        bucket_prize_list[i] = nice_no
        excess += bucket_prize_list[i]*bucket_size_list[i]
    excess = pot_size-excess
    return excess, bucket_prize_list

# Once the ideal amount of prizes have been distributed, some amount will remain
# So to protect the niceness of the pool size, we will violate some constraints


def allocate_excess_funds(excess, bucket_size_list, bucket_prize_list):
    n = len(bucket_size_list)
    for i in range(n-1):
        if bucket_prize_list[i] == bucket_prize_list[i+1]:
            incrementer = ((bucket_prize_list[i+1]+bucket_prize_list[i-1])/2-bucket_prize_list[i])*bucket_size_list[i]
            if incrementer <= excess:
                bucket_prize_list[i] = (bucket_prize_list[i+1]+bucket_prize_list[i-1])/2
                excess -= incrementer
    if excess >= 0:
        index = 0
        for i in range(n):
            if bucket_size_list[i] != 1:
                index = i
                break
        bucket_prize_list[index-1] += excess
        if bucket_prize_list[index-1] % 10 == 0:
            bucket_prize_list[index-1] = int(bucket_prize_list[index-1])
        for i in range(index-1, 0, -1):
            if bucket_prize_list[i] > bucket_prize_list[i-1]:
                bucket_prize_list[i], bucket_prize_list[i-1] = bucket_prize_list[i-1], bucket_prize_list[i]
    return bucket_prize_list


# Ties together all components into a neat and clean solution


def heuristic_solution(pot_size, entry_fee, p1, number_winners, r_max):
    bucket_size_list = calculate_bucket_sizes(number_winners, r_max)
    bucket_prize_list = calculate_prizes(pot_size, entry_fee, number_winners, p1, bucket_size_list)
    excess, bucket_prize_list = nice_numerator(pot_size, bucket_size_list, bucket_prize_list)
    bucket_prize_list = allocate_excess_funds(excess, bucket_size_list, bucket_prize_list)
    pretty_print(bucket_size_list, bucket_prize_list)
