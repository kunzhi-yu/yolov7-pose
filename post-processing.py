import pandas as pd

def ma(lst, win_size = 9):
    averages = [
        sum(lst[i:i+win_size]) / win_size
        for i in range(len(lst) - win_size + 1)
    ]
    result = [round(avg + 0.5) for avg in averages]
    result.extend(lst[:(win_size // 2)])
    result.extend(lst[-(win_size // 2):])

    return result


def label_sequence(lst):
    rm_zeros = [x if x != 1 else 0 for x in lst]
    result = []
    is_empty = True  # Start with "empty" for the first sequence of 0s
    in_zero_sequence = False  # Tracks whether we're in a sequence of 0s

    for num in rm_zeros:
        if num >= 2:
            result.append("p")
            in_zero_sequence = False  # We're no longer in a sequence of 0s
        else:
            if not in_zero_sequence:
                # We are starting a new sequence of 0s, so alternate between "empty" and "scan"
                if is_empty:
                    result.append("e")
                else:
                    result.append("s")
                # Flip the flag for the next sequence of 0s
                is_empty = not is_empty
                in_zero_sequence = True
            else:
                # We're still in the same sequence of 0s, keep the same label
                result.append(result[-1])

    return result


def identify_discharge(lst):
    result = []
    is_empty = True  # Start with "empty" for the first sequence of ps
    in_p_sequence = False  # Tracks whether we're in a sequence of ps

    for num in lst:
        if num != "p":
            result.append(num)
            in_p_sequence = False  # We're no longer in a sequence of ps
        else:
            if not in_p_sequence:
                # We are starting a new sequence of ps, so alternate between "p" and "d"
                if is_empty:
                    result.append("p")
                else:
                    result.append("d")
                # Flip the flag for the next sequence of ps
                is_empty = not is_empty
                in_p_sequence = True
            else:
                # We're still in the same sequence of ps, keep the same label
                result.append(result[-1])

    return result


def identify_os(og_lst, anno_lst):
    result = anno_lst[:]
    n = len(anno_lst)
    i = 0

    while i < n:
        # Find an e to start
        if result[i] == 'e':
            start = i
            i += 1

            # Check for a sequence of 1s until another e
            while i < n and og_lst[i] == 1:
                i += 1

            # If the sequence ends with a e, replace 1s with os
            if i < n and result[i] == 'e':
                for j in range(start + 1, i):
                    result[j] = 'o'

        else:
            i += 1

    return result


def verify_ps(og_lst, anno_lst):
    result = anno_lst[:]
    n = len(anno_lst)
    i = 0

    while i < n:
        # Find an e to start
        if result[i] == 'e':
            start = i
            i += 1

            # Check for a sequence of 1s until another e
            while i < n and og_lst[i] == 1:
                i += 1

            # If the sequence ends with a p, replace es with ps
            if i < n and result[i] == 'p':
                for j in range(start + 1, i):
                    result[j] = 'p'

        else:
            i += 1

    return result


def verify_ds(og_lst, anno_lst):
    result = anno_lst[:]
    n = len(anno_lst)
    i = 0

    while i < n:
        # Find an d to start
        if result[i] == 'd':
            start = i
            i += 1

            # Check for a sequence of 1s until another e
            while i < n and og_lst[i] == 1:
                i += 1

            # If the sequence ends with an e, replace es with ds
            if i < n and result[i] == 'e':
                for j in range(start + 1, i):
                    result[j] = 'd'

        else:
            i += 1

    return result


def main(raw_data):
    if isinstance(raw_data, str):
        df = pd.read_csv(raw_data)
        data = df['yolo_detections'].tolist()
    elif isinstance(raw_data, list):
        data = raw_data
    else:
        raise ValueError("Input must be YOLO output csv path or list type")

    # Identifies prep, scan, and discharge
    s_1 = identify_discharge(label_sequence(ma(data)))
    # Identifies other activites
    s_2 = identify_os(data, s_1)
    # Cleans up edge cases about prep and discharge
    s_3 = verify_ps(data, s_2)
    s_4 = verify_ds(data, s_3)

    if 'df' in locals():
        df['inference'] = s_4
        df.to_csv("output_videos/out.csv")
        return "csv saved"
    else:
        return s_4


if __name__ == "__main__":
    main("output_videos/2023-08-07 01-00-50 raw.csv")

    # Example usage:
    sample_data = [0, 0, 0, 1, 1, 2, 2, 2, 1, 1, 0, 1, 0, 0, 2, 2, 1, 1, 0, 0, 1, 3, 1, 0, 1, 2, 3, 3, 0, 0, 1, 0]
