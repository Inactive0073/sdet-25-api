package db

import (
	"context"
	"fmt"
	"server-test/intermal/config"

	"github.com/jackc/pgx/v5"
)

func NewConnection(cfg *config.Config) (*pgx.Conn, error) {
	dns := fmt.Sprintf("postgres://%s:%s@%s:%d/%s", cfg.DB.User, cfg.DB.Password, cfg.DB.Host, cfg.DB.Port, cfg.DB.DB)

	config, err := pgx.ParseConfig(dns)
	if err != nil {
		return nil, err
	}

	conn, err := pgx.ConnectConfig(context.Background(), config)
	if err != nil {
		return nil, err
	}

	return conn, nil
}
