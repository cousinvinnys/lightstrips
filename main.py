if __name__ == '__main__':
    print("In main")
    light_thread = Thread(target=run_lights, args=(lights, ), daemon=True)
    light_thread.start()
    # with concurrent.futures.ThreadPoolExecutor() as executor:
    #     results = executor.submit(run_lights, lights)

    app.run(host='0.0.0.0', port=5000, debug=True)