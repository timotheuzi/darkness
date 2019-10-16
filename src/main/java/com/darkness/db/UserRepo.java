package com.darkness.db;

import org.springframework.data.repository.CrudRepository;

public interface UserRepo extends CrudRepository<UserDB, Integer> {
	UserDB FindByName(String name);

	UserDB FindByLocation(Integer location);
}