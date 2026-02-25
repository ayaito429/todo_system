-- 既存ユーザーのパスワードを更新（email で特定）
UPDATE users
SET
  password = '$argon2id$v=19$m=65536,t=3,p=4$2/sfwzindG6t9d6bcy4FQA$BGKnSYZXHcGPi/g3giLyV3/TSaBxootnMliCPehFWOM',
  updated_at = NOW()
WHERE email = 'test_user@example.com';

UPDATE users
SET
  password = '$argon2id$v=19$m=65536,t=3,p=4$2/sfwzindG6t9d6bcy4FQA$BGKnSYZXHcGPi/g3giLyV3/TSaBxootnMliCPehFWOM',
  updated_at = NOW()
WHERE email = 'test_leader@example.com';

UPDATE users
SET
  password = '$argon2id$v=19$m=65536,t=3,p=4$2/sfwzindG6t9d6bcy4FQA$BGKnSYZXHcGPi/g3giLyV3/TSaBxootnMliCPehFWOM',
  updated_at = NOW()
WHERE email = 'test_admin@example.com';
