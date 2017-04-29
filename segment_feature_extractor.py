
def rough_trial(all_inkml):
    """
    Temporary.
    Segments each stroke as a new symbol
    :param all_inkml:
    :return:
    """

    for inkml in all_inkml:
        for trace_id in inkml.strokes.keys():
            inkml.create_object([trace_id])

