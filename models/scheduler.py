class Scheduler:
    def calculate_dp(self, materials, max_time):
        # setup variabel buat DP
        dp = [0] * (max_time + 1)
        item_count = [{} for _ in range(max_time + 1)]
        
        for m in materials:
            for count_arr in item_count:
                count_arr[m['name']] = 0

        # proses cari kombinasi terbaik pake Dynamic Programming
        for w in range(max_time + 1):
            for material in materials:
                time = material['time_per_kg']
                val = material['value_per_kg']
                name = material['name']
                max_qty = material['max_qty']

                if time <= w:
                    prev_w = w - time
                    current_qty_used = item_count[prev_w].get(name, 0)
                    
                    if current_qty_used < max_qty:
                        new_val = dp[prev_w] + val
                        if new_val > dp[w]:
                            dp[w] = new_val
                            item_count[w] = dict(item_count[prev_w])
                            item_count[w][name] = item_count[prev_w].get(name, 0) + 1

        # cari profit tertingginya
        max_val = 0
        best_w = 0
        for w in range(max_time + 1):
            if dp[w] >= max_val:
                max_val = dp[w]
                best_w = w

        # rekap dan format hasil akhir DP
        total_weight = 0
        details = []
        for name, qty in item_count[best_w].items():
            total_weight += qty
            if qty > 0:
                details.append({'name': name, 'qty': qty})

        return {
            'method': 'Dynamic Programming',
            'total_weight': total_weight,
            'total_time': best_w,
            'total_value': max_val,
            'details': details
        }

    def calculate_round_robin(self, materials, max_time):
        # setup variabel buat Round Robin
        time_used = 0
        total_value = 0
        total_weight = 0
        processed = {}
        
        for m in materials:
            processed[m['name']] = 0

        done = False

        # bagi rata jatah waktu ke masing-masing material
        while not done:
            processed_in_cycle = 0

            for material in materials:
                name = material['name']
                time = material['time_per_kg']
                val = material['value_per_kg']
                max_qty = material['max_qty']

                if processed[name] < max_qty:
                    if time_used + time <= max_time:
                        processed[name] += 1
                        time_used += time
                        total_value += val
                        total_weight += 1
                        processed_in_cycle += 1

            if processed_in_cycle == 0:
                done = True

        # rekap dan format hasil akhir Round Robin
        details = []
        for name, qty in processed.items():
            if qty > 0:
                details.append({'name': name, 'qty': qty})

        return {
            'method': 'Round-Robin',
            'total_weight': total_weight,
            'total_time': time_used,
            'total_value': total_value,
            'details': details
        }
