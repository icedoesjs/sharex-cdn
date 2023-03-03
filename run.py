from app import site

if __name__ == '__main__':
    # Production host gets set to 0.0.0.0 to allow all ips not just localhost
    site.run(host='0.0.0.0', threaded=True)