from flask import Flask, render_template, request, redirect, flash
from sql_query import *

app = Flask(__name__)


match_sign_up = [
    {"name": "Match Sign Up 1", "details": "Details for Match Sign Up 1"},
    {"name": "Match Sign Up 2", "details": "Details for Match Sign Up 2"},
    {"name": "Match Sign Up 3", "details": "Details for Match Sign Up 3"}
]
global_user_uid = "Uid1"

@app.route('/')
def index():
    print("LOG: Index page")
    df = query_database(get_query_profile_details(global_user_uid))
    first_name = df.iloc[0, 1]
    last_name = df.iloc[0, 2]
    birthdate = df.iloc[0, 4]
    age = df.iloc[0, 5]
    email = df.iloc[0, 6]
    genre = df.iloc[0, 7]
    category = df.iloc[0, 8]
    laptop = df.iloc[0, 10]

    profile_details = {
        "profile_name": first_name + " " + last_name,
        "age": age,
        "email": email,
        "genre": genre,
        "category": category,
        "laptop": laptop
    }

    game_recs = query_database(get_query_game_rec(global_user_uid))
    game_pop_recs = query_database(get_query_game_rec_pop())
    top_three_game_recs = game_recs.head(3)
    top_three_game_recs_pop = game_pop_recs.head(3)
    game_recs_dict = []
    game_recs_pop_dict = []

    for index, row in top_three_game_recs.iterrows():
        game_recs_dict.append( {
            'title': row[2], 
            'price': row[3],
            'category': row[4], 
            'genre': row[5]
        })


    for index, row in top_three_game_recs_pop.iterrows():
        game_recs_pop_dict.append( {
            'title': row[1], 
            'price': row[2],
            'genre': row[4],
            'popularity': row[5] 
        })
    

    df = query_database(get_query_matches()) 
    #matches_df = df[df.iloc[:, 4] == '2023-12-02'].head(3)
    matches_df = df.head(3)

    live_matches = []

    for index, row in matches_df.iterrows():
        live_matches.append( {
            'name': row[0], 
            'game_id': row[3], 
            'team_1': row[2],
            'team_2': row[6], 
            'status': row[5]
        })
  

    return render_template('index.html',
                           live_matches=live_matches,
                           profile_details=profile_details,
                           game_recommendations=game_recs_dict,
                           game_recommendations_pop=game_recs_pop_dict,
                           match_sign_up=match_sign_up)

@app.route('/login', methods=['GET','POST'])
def login():
    print("LOG: Login page")
    global global_user_uid

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        df = query_database(get_query_user_login_validation(username, password))

        if not df.empty:
            print("LOG: Login correct")
            global_user_uid = username
            return redirect('/')
        else:
            print("LOG: Login incorrect")
            return redirect('/login')
        
    return render_template('login.html')

@app.route('/update_profile_details', methods=['GET', 'POST'])
def update_profile_details():

    if request.method == 'POST':
        print("LOG: Update profile details POST")
        updated_name = request.form['profile_name']
        updated_date = request.form['date']
        updated_email = request.form['email']
        updated_genre = request.form['preferred_genre']
        updated_category = request.form['preferred_category']
        updated_laptop = request.form['current_laptop']


        update_database(update_query_profile_details(global_user_uid, updated_name.split()[0], updated_name.split()[1], updated_email, updated_genre, updated_category))
        return redirect('/')

    print("LOG: Update profile details GET")
    df = query_database(get_query_profile_details(global_user_uid))

    user_details = {
        "profile_name": df.iloc[0, 1] + " " + df.iloc[0, 2],
        "date": df.iloc[0, 4],
        "email": df.iloc[0, 6],
        "preferred_genre": df.iloc[0, 7],
        "preferred_category": df.iloc[0, 8],
    }
    return render_template('profile_details.html', user=user_details)

@app.route('/update_laptop_details', methods=['GET', 'POST'])
def update_laptop_details():

    if request.method == 'GET':
        df = query_database(get_query_all_laptops())
        df['concatenated'] = df.apply(lambda row: ' '.join(map(str, row)), axis=1)
        return render_template('laptop_details.html', laptop_options=df['concatenated'].tolist())
    elif request.method == 'POST':
        df = query_database(get_query_all_laptops())
        selected_index = int(request.form['selected_laptop']) 
        laptop_id = df.iloc[selected_index,0]
        print(f"LOG: User selected laptop {laptop_id}")

        update_database(update_query_laptop_details(global_user_uid, laptop_id))
        print("updated")
        return redirect("/")

@app.route('/delete_laptop_from_user_profile', methods=['GET', 'POST'])
def delete_laptop_form_user_profile():
    update_database(delete_query_laptop_from_user(global_user_uid))

    return redirect("/")


@app.route('/search-results', methods=['GET'])
def search_results():
    user_search_query = request.args.get('search_query')

    results = query_database(get_query_search(user_search_query))

    mock_results = results[2][:3].tolist()
    
    return render_template('search_results.html', search_query=user_search_query, search_results=mock_results)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user_id = request.form['user_id']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password = request.form['password']
        date_of_birth = request.form['date_of_birth']
        email = request.form['email']
        preferred_genre = request.form['preferred_genre']
        preferred_category = request.form['preferred_category']
        user_type = "Individual"
        selected_laptop_id = "LP1"

        update_database(create_query_add_user(user_id, first_name, last_name, password, date_of_birth, email, preferred_genre, preferred_category, user_type, selected_laptop_id))

        return redirect("/login")
    
    return render_template('sign_up.html')

@app.route('/register_for_match', methods=['GET', 'POST'])
def register_for_team():
    if request.method == 'POST':
        team_id = request.form['team_id']
        game_id = request.form['game_id']
        match_date = request.form['match_date']
        
        result = procedure_call_database(validate_team_match(team_id, game_id, match_date))
        print(f"LOG: Register for Match result is {result}")
        
        return redirect("/")
        
    return render_template('register_for_team.html')


@app.route('/team_signup', methods=['GET', 'POST'])
def team_signup():
    if request.method == 'POST':
        team_id = request.form['team_id']
        team_name = request.form['team_name']

        result = update_database(update_query_register_new_team(team_id, team_name)) 
        print(f"LOG: Team Signup Result is {result}")
        
        return redirect("/")
        
    return render_template('team_signup.html')

@app.route('/add_user_to_existing_team', methods=['GET', 'POST'])
def add_user_to_existing_team():
    if request.method == 'POST':
        team_id = request.form['team_id']
        user_id = request.form['user_id']

        result = update_database(update_query_add_user_to_existing_team(team_id, user_id)) 
        print(f"LOG: Add user to existing team result is {result}")
        
        return redirect("/")
        
    return render_template('add_user_to_existing_team.html')

if __name__ == '__main__':
    app.run(port=8000,debug=True)