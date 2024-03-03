from website import create_app

if __name__=='__main__':
    app=create_app()
    app.run(debug=True)
    #cOMMIT
    #disable debug mode once successfully deployed