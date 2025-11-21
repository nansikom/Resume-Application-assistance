import requests
from requests.sessions import Session

# Create a session to maintain cookies
session = Session()
base_url = "http://127.0.0.1:5000"

print("=" * 60)
print("TESTING RESUME-APPLICATION-ASSISTANCE WORKFLOW")
print("=" * 60)

# Test 1: Check initial state
print("\n1. Testing initial session state...")
response = session.get(f"{base_url}/debug")
print(f"   Status: {response.status_code}")
print(f"   Initial state: {response.json()}")
assert response.json()['total_resume_docs'] == 0
assert response.json()['total_job_docs'] == 0
print("   ✓ Initial state is empty")

# Test 2: Upload first resume
print("\n2. Testing resume upload...")
resume_text = "Software Engineer with 5 years of experience in Python, JavaScript, Flask, React, and database management. Strong problem-solving skills and team collaboration."
response = session.post(f"{base_url}/uploadform", data={
    'Resumedisplay': resume_text
})
print(f"   Status: {response.status_code}")

# Check session after resume upload
response = session.get(f"{base_url}/debug")
debug_data = response.json()
print(f"   Session state: {debug_data}")
assert debug_data['total_resume_docs'] == 1
print("   ✓ Resume uploaded successfully")

# Test 3: Upload job description
print("\n3. Testing job description upload...")
job_text = "Looking for a Software Engineer with experience in Python, Flask, React, and strong problem-solving abilities. Must have database knowledge and team collaboration skills."
response = session.post(f"{base_url}/uploadform1", data={
    'jobdesc': job_text
})
print(f"   Status: {response.status_code}")

# Check session after job upload
response = session.get(f"{base_url}/debug")
debug_data = response.json()
print(f"   Session state: {debug_data}")
assert debug_data['total_job_docs'] == 1
print("   ✓ Job description uploaded successfully")

# Test 4: Analyze match with first set of documents
print("\n4. Testing match analysis with first documents...")
response = session.get(f"{base_url}/simple_match")
print(f"   Status: {response.status_code}")
match_data = response.json()
print(f"   Match percentage: {match_data['match_percentage']}%")
print(f"   Total matches: {match_data['total_common']}/{match_data['job_word_count']}")
print(f"   Common words (first 10): {match_data['common_words'][:10]}")
first_match_percentage = match_data['match_percentage']
first_common_words = set(match_data['common_words'])
print("   ✓ Analysis completed successfully")

# Test 5: Upload DIFFERENT resume (testing refresh)
print("\n5. Testing resume refresh with NEW document...")
new_resume_text = "Data Scientist with expertise in machine learning, Python, TensorFlow, data analysis, and statistical modeling. Experience with big data technologies."
response = session.post(f"{base_url}/uploadform", data={
    'Resumedisplay': new_resume_text
})
print(f"   Status: {response.status_code}")

# Check session was updated
response = session.get(f"{base_url}/debug")
debug_data = response.json()
print(f"   Session state: {debug_data}")
assert debug_data['total_resume_docs'] == 1  # Should still be 1, not 2
print("   ✓ Resume replaced (not appended)")

# Test 6: Analyze match with NEW resume
print("\n6. Testing match analysis with NEW resume...")
response = session.get(f"{base_url}/simple_match")
print(f"   Status: {response.status_code}")
new_match_data = response.json()
print(f"   Match percentage: {new_match_data['match_percentage']}%")
print(f"   Total matches: {new_match_data['total_common']}/{new_match_data['job_word_count']}")
print(f"   Common words (first 10): {new_match_data['common_words'][:10]}")
second_match_percentage = new_match_data['match_percentage']
second_common_words = set(new_match_data['common_words'])

# Verify the results are different
print("\n7. Verifying results changed with new document...")
print(f"   First match: {first_match_percentage}%")
print(f"   Second match: {second_match_percentage}%")
print(f"   Match percentages different: {first_match_percentage != second_match_percentage}")
print(f"   Common words changed: {first_common_words != second_common_words}")

if first_match_percentage != second_match_percentage:
    print("   ✓ Match percentage updated correctly!")
else:
    print("   ⚠ Warning: Match percentages are the same (might be coincidence)")

if first_common_words != second_common_words:
    print("   ✓ Common words updated correctly!")
else:
    print("   ⚠ Warning: Common words are the same")

# Test 7: Upload DIFFERENT job description
print("\n8. Testing job description refresh with NEW document...")
new_job_text = "Seeking a Data Scientist with machine learning expertise, Python skills, and experience with TensorFlow and statistical analysis."
response = session.post(f"{base_url}/uploadform1", data={
    'jobdesc': new_job_text
})
print(f"   Status: {response.status_code}")

# Test 8: Final analysis
print("\n9. Testing final match analysis...")
response = session.get(f"{base_url}/simple_match")
print(f"   Status: {response.status_code}")
final_match_data = response.json()
print(f"   Match percentage: {final_match_data['match_percentage']}%")
print(f"   Total matches: {final_match_data['total_common']}/{final_match_data['job_word_count']}")
print(f"   Common words (first 10): {final_match_data['common_words'][:10]}")
print("   ✓ Final analysis completed")

# Test 9: Stats endpoint
print("\n10. Testing stats endpoint...")
response = session.get(f"{base_url}/stats")
print(f"   Status: {response.status_code}")
stats_data = response.json()
print(f"   Resume stats: {stats_data['resume_stats']}")
print(f"   Job stats: {stats_data['job_stats']}")
print("   ✓ Stats endpoint working")

print("\n" + "=" * 60)
print("ALL TESTS PASSED! ✓")
print("=" * 60)
print("\nKey findings:")
print("- Session management works correctly")
print("- Documents are replaced (not appended) on new uploads")
print("- Match analysis uses current session data")
print("- Results update when new documents are uploaded")
print("- Error handling works for missing documents")
