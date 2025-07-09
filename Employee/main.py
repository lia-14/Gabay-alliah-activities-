from flask import Flask, jsonify, request, render_template, redirect, url_for,session,send_file
from flask_mysqldb import MySQL
import hashlib
import os
import csv
import io

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'employee_db'
mysql = MySQL(app)

SALT = 'haysssss'

app.secret_key = os.urandom(24)



# ----------Home Page------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check-user', methods=['POST'])
def check_user():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'success': False, 'message': 'Please enter both username and password'}), 400

        cur = mysql.connection.cursor()

        # Check admin table first
        cur.execute("SELECT * FROM admin WHERE username = %s", (username,))
        admin = cur.fetchone()
        if admin:
            salted = str(SALT + password).encode('utf-8')
            hashed = hashlib.sha512(salted).hexdigest()
            if admin[1] == hashed:
                session['logged_in'] = True
                session['username'] = username
                session['role'] = 'admin'
                cur.close()
                return jsonify({'success': True, 'message': 'Admin login successful!', 'redirect': '/admin-dashboard'})
            else:
                cur.close()
                return jsonify({'success': False, 'message': 'Invalid username or password'}), 401

        # Check employee table
        cur.execute("SELECT * FROM employee_db WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()

        if not user:
            return jsonify({'success': False, 'message': 'Invalid username or password'}), 401

        salted = str(SALT + password).encode('utf-8')
        hashed = hashlib.sha512(salted).hexdigest()

        if user[2] != hashed:  # user[2] is the password column
            return jsonify({'success': False, 'message': 'Invalid username or password'}), 401

        # user[8] is the role column (assuming your table columns are: id, username, password, name, address, age, gender, position, role, created_at)
        role = user[8]

        session['logged_in'] = True
        session['username'] = username
        session['role'] = role

        if role == 'admin':
            return jsonify({'success': True, 'message': 'Admin login successful!', 'redirect': '/admin-dashboard'})
        else:
            return jsonify({'success': True, 'message': 'Login successful!', 'redirect': '/dashboard'})

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/dashboard')
def dashboard():

    if not session.get('logged_in'):
        return redirect(url_for('index'))
    return render_template('employee-dashboard.html', username=session.get('username'))


# ----------Logout------------
@app.route('/logout', methods=['POST'])
def logout():
    try:

        session.clear()
        return jsonify({
            'success': True,
            'message': 'Logged out successfully',
            'redirect': '/'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500




# Get Employee Info
@app.route('/get-employee-info')
def get_employee_info():
    try:
        if not session.get('logged_in'):
            return jsonify({
                "success": False,
                "error": "Not logged in"
            }), 401

        username = session.get('username')
        
        cur = mysql.connection.cursor()
        try:
            cur.execute("""
                SELECT id, username, name, address, age, gender, position
                FROM employee_db
                WHERE username = %s
            """, (username,))
            
            result = cur.fetchone()
            
            if result:
                employee_info = {
                    'id': result[0],
                    'username': result[1],
                    'name': result[2],
                    'address': result[3],
                    'age': result[4],
                    'gender': result[5],
                    'position': result[6]
                }
                return jsonify({
                    'success': True,
                    'employee_info': employee_info
                })
            else:
                return jsonify({
                    'success': False,
                    'error': "Employee information not found"
                }), 404
                
        except Exception as e:
            return jsonify({
                'success': False,
                'error': f"Database error: {str(e)}"
            }), 500
        finally:
            cur.close()
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f"Server error: {str(e)}"
        }), 500


#Admin Dashboard
@app.route('/admin-dashboard')
def admin_dashboard():

    if not session.get('logged_in') or session.get('role') != 'admin':
        return redirect(url_for('index'))
    return render_template('dashboard.html', username=session.get('username'))


# Check Session
@app.route('/check-session', methods=['GET'])
def check_session():
    return jsonify({
        'logged_in': session.get('logged_in', False),
        'username': session.get('username', None)
    })





# Register Route
@app.route('/register-page')
def register_page():
    return render_template('register.html')


# ----------Add Employee------------
@app.route('/add-employee', methods=['POST'])
def add_employee():
    try:
        if not session.get('logged_in') or session.get('role') != 'admin':
            return jsonify({"error": "Unauthorized"}), 401

        data = request.get_json()
        cur = mysql.connection.cursor()

        username = data.get('username').strip() if data.get('username') else data['name'].replace(" ", ".").lower()
        password = data.get('password') or "default123"
        salted = str(SALT + password).encode('utf-8')
        hashed = hashlib.sha512(salted).hexdigest()

        try:
            cur.execute("SELECT username FROM employee_db WHERE username = %s", (username,))
            if cur.fetchone():
                return jsonify({
                    'success': False,
                    'error': 'Username already exists'
                }), 400

            cur.execute("""
                INSERT INTO employee_db 
                (username, password, name, address, age, gender, position, role)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                username,
                hashed,
                data['name'],
                data['address'],
                data['age'],
                data['gender'],
                data['position'],
                data['role']
            ))

            mysql.connection.commit()

            return jsonify({
                'success': True,
                'message': f'Employee added successfully.\nUsername: {username}\nPassword: {password}'
            })
        except Exception as e:
            mysql.connection.rollback()
            return jsonify({
                'success': False,
                'error': f'Database error: {str(e)}'
            }), 500
        finally:
            cur.close()

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500




# ----------Edit Employee------------
@app.route('/edit-employee', methods=['POST'])
def edit_employee():
    try:
        if not session.get('logged_in') or session.get('role') != 'admin':
            return jsonify({"error": "Unauthorized"}), 401

        data = request.get_json()
        employee_id = data.get('id')
        password = data.get('password')

        cur = mysql.connection.cursor()
        try:
            cur.execute("SELECT username FROM employee_db WHERE id = %s", (employee_id,))
            result = cur.fetchone()
            if not result:
                return jsonify({
                    'success': False,
                    'error': 'Employee not found'
                }), 404

            current_username = result[0]
            new_username = data.get('username')

            cur.execute("SET FOREIGN_KEY_CHECKS=0")
            cur.execute("START TRANSACTION")

            try:
                cur.execute("""
                    UPDATE employee_db
                    SET name = %s, address = %s, age = %s, gender = %s, position = %s, username = %s, role = %s
                    WHERE id = %s
                """, (
                    data['name'],
                    data['address'],
                    data['age'],
                    data['gender'],
                    data['position'],
                    new_username,
                    data['role'],
                    employee_id
                ))

                update_query = """
                    UPDATE employee_db
                    SET username = %s
                """
                params = [new_username]

                if password and password.strip():
                    salted = str(SALT + password).encode('utf-8')
                    hashed = hashlib.sha512(salted).hexdigest()
                    update_query += ", password = %s"
                    params.append(hashed)

                update_query += " WHERE id = %s"
                params.append(employee_id)

                cur.execute(update_query, tuple(params))

                cur.execute("SET FOREIGN_KEY_CHECKS=1")
                mysql.connection.commit()

                return jsonify({
                    'success': True,
                    'message': 'Employee information updated successfully'
                })

            except Exception as e:
                cur.execute("SET FOREIGN_KEY_CHECKS=1")
                mysql.connection.rollback()
                raise e

        except Exception as e:
            print(f"Database error during edit: {str(e)}")
            return jsonify({
                'success': False,
                'error': f'Database error: {str(e)}'
            }), 500
        finally:
            cur.close()

    except Exception as e:
        print(f"Server error during edit: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


# Delete Employee
@app.route('/delete-employee', methods=['POST'])
def delete_employee():
    try:
        if not session.get('logged_in') or session.get('role') != 'admin':
            return jsonify({"error": "Unauthorized"}), 401

        data = request.get_json()
        employee_id = data.get('id')

        cur = mysql.connection.cursor()
        try:
            cur.execute("SELECT username FROM employee_db WHERE id = %s", (employee_id,))
            result = cur.fetchone()
            if not result:
                return jsonify({
                    'success': False,
                    'error': 'Employee not found'
                }), 404

            username = result[0]

            cur.execute("DELETE FROM employee_db WHERE id = %s", (employee_id,))
            mysql.connection.commit()
            return jsonify({
                'success': True,
                'message': 'Employee deleted successfully'
            })
        except Exception as e:
            mysql.connection.rollback()
            return jsonify({
                'success': False,
                'error': f'Database error: {str(e)}'
            }), 500
        finally:
            cur.close()

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Register 
@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        name = data.get('name')
        address = data.get('address')
        age = data.get('age')
        gender = data.get('gender')
        position = data.get('position')
        role = data.get('role')  # Added role

        # Check all fields
        if not all([username, password, name, address, age, gender, position, role]):
            return jsonify({
                'success': False,
                'message': 'All fields are required'
            })

        cur = mysql.connection.cursor()

        # Check if username exists
        cur.execute("SELECT * FROM employee_db WHERE username = %s", (username,))
        if cur.fetchone():
            return jsonify({
                'success': False,
                'message': 'Username already exists'
            })

        try:
            cur.execute("START TRANSACTION")
            salted = str(SALT + password).encode('utf-8')
            hashed = hashlib.sha512(salted).hexdigest()

            cur.execute("""
                INSERT INTO employee_db 
                (username, password, name, address, age, gender, position, role)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (username, hashed, name, address, age, gender, position, role))

            mysql.connection.commit()

            # Set up session for automatic login
            session['logged_in'] = True
            session['username'] = username
            session['role'] = role  # Use the selected role

            return jsonify({
                'success': True,
                'message': 'Registration successful!',
                'redirect': '/dashboard'
            })

        except Exception as e:
            mysql.connection.rollback()
            raise e

        finally:
            cur.close()

    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500
    
    # ----------Get All Employees------------
@app.route('/get-all-employees')
def get_all_employees():
    try:
        if not session.get('logged_in') or session.get('role') != 'admin':
            return jsonify({"success": False, "error": "Unauthorized"}), 401

        cur = mysql.connection.cursor()
        try:
            cur.execute("""
                SELECT id, name, address, age, gender, position, username, role
                FROM employee_db
                ORDER BY id ASC
            """)
            results = cur.fetchall()
            employees = []
            for row in results:
                employees.append({
                    "id": row[0],
                    "name": row[1],
                    "address": row[2],
                    "age": row[3],
                    "gender": row[4],
                    "position": row[5],
                    "username": row[6],
                    "role": row[7]
                })
            return jsonify({"success": True, "employees": employees})
        except Exception as e:
            return jsonify({"success": False, "error": f"Database error: {str(e)}"}), 500
        finally:
            cur.close()
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
if __name__ == '__main__':
    app.run(debug=True)
